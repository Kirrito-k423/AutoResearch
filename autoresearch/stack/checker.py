"""autoresearch.stack.checker — 库检测 + conda env 探测 + 1-step 干跑 (D-39..D-42).

核心入口 `check_stack(spec, libs=("verl", "veomni"))`:
  1. probe_conda_env: 远程 `conda env list | grep <env>` 验 env 存在 (D-40)
  2. check_library: 远程 `conda run -n <env> python -c "import <lib>; print(...)"` (D-39)
  3. run_one_step_dryrun: 1-step NPU 干跑, 30s timeout (D-41)
  4. 汇总 -> StackResult

不引第三方客户端 (D-39 决策): 用裸 curl 等价 (python -c) + workspace_core.ssh.SSHClient.
不写新 dep.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from workspace_core.config import ServerSpec, from_path, ConfigError
from workspace_core.progress import emit_progress
from workspace_core.ssh import (
    AuthError,
    BootstrapFailed,
    HostSpec,
    SSHClient,
    SSHError,
)
from workspace_core.ssh.exceptions import CommandTimeoutError

from .models import (
    CondaEnvProbe,
    LibraryCheck,
    OneStepResult,
    StackResult,
    StackSummary,
)

# === Constants ===

DEFAULT_LIBS: tuple[str, ...] = ("verl", "veomni")
ONE_STEP_TIMEOUT_S: float = 30.0
DEFAULT_CHECK_TIMEOUT_S: float = 12.0

# D-41 1-step 脚本 (NPU 适配 — 用户明确要求 torch_npu, 不是 verl.trainer.main)
# 用 {lib} 占位符供 check_stack 替换
ONE_STEP_SCRIPT_TMPL = """\
import torch, torch_npu, {lib}
x = torch.randn(2, 3).npu()
y = (x + 1).sum()
print("SUM=", y.item())
print("NPU_COUNT=", torch_npu.npu.device_count())
"""

DIAG_ENV_MISSING_TMPL = (
    "conda env '{env}' 不在远程服务器上; 请先 `conda env create -f <env>.yml` 或在 config 中配正确 env 名"
)
DIAG_IMPORT_FAIL_TMPL = (
    "env '{env}' 存在但 {lib} 不可 import; 检查 pip install 是否在 {env} 内"
)
DIAG_ONE_STEP_TIMEOUT_TMPL = (
    "1-step 干跑 > {timeout}s 超时; NPU 通信问题, 先跑 `autoresearch hw probe --server {server}`"
)
DIAG_ONE_STEP_NO_OUTPUT = "1-step 干跑 stdout 无 SUM=; 检查 torch_npu / {lib} 是否同 env"

# === Server / SSH helpers ===

def _resolve_server(server_name: str, config_path: str | Path | None) -> ServerSpec:
    cfg = from_path(str(config_path) if config_path else None)
    spec = next((s for s in cfg.servers if s.name == server_name), None)
    if spec is None:
        avail = [s.name for s in cfg.servers]
        raise ConfigError(
            f"config.servers 中找不到 '{server_name}'; 已配: {avail}"
        )
    return spec


def _host_spec(spec: ServerSpec) -> HostSpec:
    id_file = None
    if spec.identity_file:
        id_file = str(Path(spec.identity_file).expanduser())
    return HostSpec(
        alias=spec.name,
        host=spec.host,
        port=spec.port,
        user=spec.user,
        identity_file=id_file,
    )


def _ssh_exec_capture(
    spec: ServerSpec,
    command: str,
    timeout: float = DEFAULT_CHECK_TIMEOUT_S,
) -> tuple[int, str, str]:
    from workspace_core.secrets import resolve_secret
    pw = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    client = SSHClient(
        _host_spec(spec),
        bootstrap_password=pw,
    )
    try:
        client.connect(connect_timeout=5.0)
    except (AuthError, SSHError) as e:
        raise BootstrapFailed(f"SSH 连接失败: {e}") from e
    try:
        return client.exec(command, timeout=timeout)
    finally:
        client.close()


# === Remote command builders ===

def _python_exec_prefix(spec: ServerSpec) -> str:
    """构造 `conda run -n <env> python -c "..."` 前缀, 或裸 `python -c "..."`."""
    if spec.conda_env:
        return f"conda run -n {spec.conda_env} python -c "
    return "python -c "


def _shell_quote_double(s: str) -> str:
    """shell 双引号转义, 包外双引号."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _check_library_command(spec: ServerSpec, lib: str) -> str:
    """构造 `python -c "import <lib>; print(<lib>.__version__)"` 命令."""
    inner = f"import {lib}\nprint({lib}.__version__)"
    return _python_exec_prefix(spec) + _shell_quote_double(inner)


def _conda_env_list_command() -> str:
    """`conda env list` 输出含所有 env 名 + python 路径."""
    return "conda env list"


def _one_step_command(spec: ServerSpec, lib: str) -> str:
    """构造 1-step NPU 干跑命令 (D-41, 用户明确要求 torch_npu)."""
    inner = ONE_STEP_SCRIPT_TMPL.format(lib=lib)
    return _python_exec_prefix(spec) + _shell_quote_double(inner)


# === Checks ===

def probe_conda_env(spec: ServerSpec) -> CondaEnvProbe:
    """远程 `conda env list`, 解析 spec.conda_env 是否存在."""
    name = spec.conda_env
    if not name:
        return CondaEnvProbe(
            name="", exists=False, python_version=None,
            detail="config.conda_env 未配, 走系统 python",
        )
    try:
        ec, so, se = _ssh_exec_capture(spec, _conda_env_list_command())
    except Exception as e:
        return CondaEnvProbe(
            name=name, exists=False, python_version=None,
            detail=f"conda env list 失败: {e}",
        )
    if ec != 0:
        return CondaEnvProbe(
            name=name, exists=False, python_version=None,
            detail=f"conda env list exit={ec}: {se.strip()[:200]}",
        )
    # 解析 conda env list 输出: 行如 "verl-env    /opt/conda/envs/verl-env"
    pattern = rf"^{re.escape(name)}\s+(\S+)"
    for line in so.splitlines():
        m = re.match(pattern, line.strip())
        if m:
            return CondaEnvProbe(
                name=name, exists=True, python_version=None, detail=None,
            )
    return CondaEnvProbe(
        name=name, exists=False, python_version=None,
        detail=DIAG_ENV_MISSING_TMPL.format(env=name),
    )


def check_library(spec: ServerSpec, lib: str) -> LibraryCheck:
    """远程 `python -c "import <lib>; print(<lib>.__version__)"` (D-39)."""
    t0 = time.perf_counter()
    try:
        ec, so, se = _ssh_exec_capture(spec, _check_library_command(spec, lib))
    except Exception as e:
        latency = int((time.perf_counter() - t0) * 1000)
        return LibraryCheck(
            library=lib, version=None, ok=False, detail=str(e)[:200], warning=None,
        )
    latency = int((time.perf_counter() - t0) * 1000)
    if ec != 0:
        detail = (se or so).strip()[:200]
        if spec.conda_env:
            return LibraryCheck(
                library=lib, version=None, ok=False,
                detail=DIAG_IMPORT_FAIL_TMPL.format(env=spec.conda_env, lib=lib) + f"; ({detail})",
                warning=None,
            )
        return LibraryCheck(
            library=lib, version=None, ok=False, detail=detail, warning=None,
        )
    # stdout 末行 = version
    version = so.strip().splitlines()[-1] if so.strip() else None
    return LibraryCheck(
        library=lib, version=version, ok=True, detail=None, warning=None,
    )


def run_one_step_dryrun(
    spec: ServerSpec,
    lib: str,
    timeout: float = ONE_STEP_TIMEOUT_S,
) -> OneStepResult:
    """远程 1-step NPU 干跑 (D-41), 30s timeout 单独传."""
    t0 = time.perf_counter()
    try:
        ec, so, se = _ssh_exec_capture(spec, _one_step_command(spec, lib), timeout=timeout)
    except CommandTimeoutError:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return OneStepResult(
            ok=False, npu_device_count=None, sum_value=None,
            elapsed_ms=elapsed, detail=None,
            warning=DIAG_ONE_STEP_TIMEOUT_TMPL.format(timeout=int(timeout), server=spec.name),
        )
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return OneStepResult(
            ok=False, npu_device_count=None, sum_value=None,
            elapsed_ms=elapsed, detail=str(e)[:200], warning=None,
        )
    elapsed = int((time.perf_counter() - t0) * 1000)
    if ec != 0:
        return OneStepResult(
            ok=False, npu_device_count=None, sum_value=None,
            elapsed_ms=elapsed, detail=(se or so).strip()[:200],
            warning=f"1-step exit={ec}, {lib} 可能 import 失败",
        )
    # 解析 SUM= / NPU_COUNT=
    sum_val = None
    npu_count = None
    for line in so.splitlines():
        line = line.strip()
        if line.startswith("SUM="):
            try:
                sum_val = float(line[4:].strip())
            except ValueError:
                pass
        elif line.startswith("NPU_COUNT="):
            try:
                npu_count = int(line[len("NPU_COUNT="):].strip())
            except ValueError:
                pass
    if sum_val is None:
        return OneStepResult(
            ok=False, npu_device_count=npu_count, sum_value=None,
            elapsed_ms=elapsed, detail=DIAG_ONE_STEP_NO_OUTPUT.format(lib=lib),
            warning="1-step stdout 无 SUM=",
        )
    return OneStepResult(
        ok=True, npu_device_count=npu_count, sum_value=sum_val,
        elapsed_ms=elapsed, detail=None, warning=None,
    )


# === Top-level entry ===

def check_stack(
    server_name: str,
    config_path: str | Path | None = None,
    libs: tuple[str, ...] = DEFAULT_LIBS,
    skip_one_step: bool = False,
    lang: str = "zh",
) -> StackResult:
    """单台 stack check 入口.

    步骤:
      1. probe_conda_env (D-40)
      2. check_library 每个 lib (D-39)
      3. run_one_step_dryrun (D-41, NPU 适配, 30s timeout)
      4. 汇总 -> StackResult

    失败诊断 (D-42): env 缺失 / import 失败 / 1-step 超时 各给可读错误.
    """
    emit_progress("stack.check.start", server=server_name)
    try:
        spec = _resolve_server(server_name, config_path)
    except ConfigError as e:
        return StackResult(
            server=server_name, ok=False, severity="fail",
            conda_env=CondaEnvProbe(name="", exists=False, python_version=None, detail=str(e)),
            libraries={},
            one_step=None,
            error=f"配置错误: {e}",
        )

    # 1. conda env 探测
    env_probe = probe_conda_env(spec)

    # 2. 库检测
    lib_checks: dict[str, LibraryCheck] = {}
    any_lib_ok = False
    for lib in libs:
        chk = check_library(spec, lib)
        lib_checks[lib] = chk
        if chk["ok"]:
            any_lib_ok = True

    # 3. 1-step 干跑 (env 在 + 至少一 lib ok 才跑)
    one_step: OneStepResult | None = None
    if env_probe["exists"] and any_lib_ok and not skip_one_step:
        # 选一个 OK 的 lib
        ok_lib = next((l for l in libs if lib_checks[l]["ok"]), libs[0])
        one_step = run_one_step_dryrun(spec, ok_lib)

    # 4. 汇总
    error_parts = []
    if not env_probe["exists"] and env_probe["name"]:
        error_parts.append(env_probe["detail"] or "conda env 不存在")
    failed_libs = [l for l, c in lib_checks.items() if not c["ok"]]
    for lib in failed_libs:
        error_parts.append(lib_checks[lib]["detail"] or f"{lib} import 失败")
    if one_step and not one_step["ok"] and one_step.get("warning"):
        error_parts.append(one_step["warning"])

    if not env_probe["exists"] and env_probe["name"]:
        severity = "fail"
        ok = False
    elif failed_libs:
        severity = "fail"
        ok = False
    elif one_step and not one_step["ok"]:
        # env OK, libs OK, 但 1-step 失败 -> warn (D-41.C6)
        severity = "warn"
        ok = True
    else:
        severity = "ok"
        ok = True

    err = "\n".join(error_parts) if error_parts else None
    return StackResult(
        server=server_name,
        ok=ok,
        severity=severity,
        conda_env=env_probe,
        libraries=lib_checks,
        one_step=one_step,
        error=err,
    )


# === CLI boundary ===

def _check_message(severity: str, lang: str) -> str:
    if lang == "en":
        return {
            "ok": "Stack check passed",
            "warn": "Stack check passed with warnings",
            "fail": "Stack check failed",
        }.get(severity, "Stack check done")
    return {
        "ok": "训练栈检查通过",
        "warn": "训练栈检查通过 (含警告)",
        "fail": "训练栈检查失败",
    }.get(severity, "训练栈检查完成")


def run_stack_check(
    server: str,
    config: str | Path | None = None,
    libs: tuple[str, ...] | None = None,
    lang: str = "zh",
) -> int:
    """CLI 边界: 单机 stack check."""
    if not libs:
        libs = DEFAULT_LIBS
    result = check_stack(server, config_path=config, libs=libs, lang=lang)
    payload = {
        "ok": result["ok"],
        "severity": result["severity"],
        "data": {
            "server": result["server"],
            "conda_env": result["conda_env"],
            "libraries": result["libraries"],
            "one_step": result["one_step"],
        },
        "message": _check_message(result["severity"], lang),
        "error": result["error"],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if result["ok"] else 1


# === --all multi-server (Phase 07-03 完整实现, 07-01 占位) ===

def run_stack_check_all(
    config: str | Path | None = None,
    libs: tuple[str, ...] | None = None,
    lang: str = "zh",
) -> int:
    """CLI 边界: --all 多机 stack check, 07-03 完整实现 (07-01 占位).

    07-01 返回 0 跟 mock 走通; 07-03 替换为 ThreadPoolExecutor 并发.
    """
    import json as _json
    if not libs:
        libs = DEFAULT_LIBS
    print(_json.dumps({
        "ok": False,
        "severity": "fail",
        "data": {
            "total": 0, "passed": 0, "failed": 0, "warned": 0,
            "passed_servers": [], "failed_servers": [],
            "results": {},
        },
        "message": "stack check --all 在 07-01 阶段是占位, 完整并发 07-03 实现",
        "error": "not_implemented",
    }, ensure_ascii=False))
    return 1
