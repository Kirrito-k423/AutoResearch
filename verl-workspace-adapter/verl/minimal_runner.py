"""verl-workspace-adapter.verl.minimal_runner — verl 1-step 干跑 (D-44).

复用 Phase 7 D-41 1-step 脚本 (torch_npu + lib).
不引 verl SDK / 训练脚本, 走 `python -c "..."` 单进程.
"""
from __future__ import annotations

import time
from typing import TypedDict

from workspace_core.config import ServerSpec
from workspace_core.ssh import CommandTimeoutError

from ..common.conda_utils import run_in_env


# === Constants ===

# D-41 1-step 脚本 (NPU 适配 — 用户明确要求 torch_npu, 不是 CUDA verl.trainer.main)
# 跟 Phase 7 autoresearch/stack/checker.py ONE_STEP_SCRIPT_TMPL 同步
ONE_STEP_SCRIPT_TMPL = """\
import torch, torch_npu, verl
x = torch.randn(2, 3).npu()
y = (x + 1).sum()
print("SUM=", y.item())
print("NPU_COUNT=", torch_npu.npu.device_count())
"""


class MinimalResult(TypedDict, total=False):
    """1-step 干跑结果 (D-44, 供 08-04 manifest 写)."""
    lib: str
    sum_value: float | None
    npu_count: int | None
    elapsed_ms: int
    exit_code: int
    stdout: str
    stderr: str
    error: str | None
    timeout: bool


def _parse_one_step_output(stdout: str) -> tuple[float | None, int | None]:
    """解析 stdout 拿 SUM= / NPU_COUNT=  (同 Phase 7 parser)."""
    sum_val = None
    npu_count = None
    for line in stdout.splitlines():
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
    return sum_val, npu_count


def run_minimal(
    spec: ServerSpec,
    conda_env: str = "",
    workdir: str = "",
    lib: str = "verl",
    timeout: float = 30.0,
) -> MinimalResult:
    """远程跑 1-step 干跑, 返回 MinimalResult (D-44).

    Args:
        spec: 目标 ServerSpec (config 中读)
        conda_env: conda env 名称 (D-40, 走 `conda run -n <env>`)
        workdir: 远程工作目录 (D-46, 走 `cd <workdir> && ...`)
        lib: 库名 (默认 verl, veomni runner 用 veomni)
        timeout: SSH exec timeout, 默认 30s (D-41)
    """
    # 用 {lib} 替换 lib 占位; 但当前模板固定为 verl, lib 走环境变量替换
    script = ONE_STEP_SCRIPT_TMPL.replace("verl", lib, 1)  # 仅替换第一次出现 (import 行)
    # 实际是 inline python -c "<script>" — 单引号包整个 script, 内嵌双引号
    # shell 转义: 单引号在 python -c 字符串里需要双引号; 简化: 用三引号 + 双引号
    safe_script = script.replace('"', '\\"').replace("\n", "; ")
    command = f'python -c "{safe_script}"'

    t0 = time.perf_counter()
    try:
        ec, so, se = run_in_env(spec, command, conda_env=conda_env, workdir=workdir, timeout=timeout)
    except CommandTimeoutError as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=True,
        )
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=False,
        )
    elapsed = int((time.perf_counter() - t0) * 1000)
    sum_val, npu_count = _parse_one_step_output(so)
    return MinimalResult(
        lib=lib, sum_value=sum_val, npu_count=npu_count, elapsed_ms=elapsed,
        exit_code=ec, stdout=so, stderr=se, error=None, timeout=False,
    )
