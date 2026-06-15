"""verl-workspace-adapter.verl.minimal_runner — verl 1-step 干跑 (D-44).

复用 Phase 7 D-41 1-step 脚本 (torch_npu + lib).
不引 verl SDK / 训练脚本, 走 `python -c "..."` 单进程.
"""
from __future__ import annotations
from pathlib import Path

import time
from typing import TypedDict

from workspace_core.config import ServerSpec
from workspace_core.ssh import CommandTimeoutError

from ..common.conda_utils import run_in_env


# === Constants ===

# D-41 1-step 脚本 (NPU 适配 — 用户明确要求 torch_npu, 不是 CUDA verl.trainer.main)
# 跟 Phase 7 autoresearch/stack/checker.py ONE_STEP_SCRIPT_TMPL 同步
# D-45 锁: 1-step 跑 wandb 离线模式, 落 <workdir>/wandb/run-<ts>-<id>/ 目录
# 跟 D-41 兼容: SUM + NPU_COUNT print 保留 (D-41 NPU 适配)
# D-45 决策: 写临时脚本到本地, SFTP 上传, 远程 bash python /tmp/<file>.py 跑
#           (不用 inline python -c 压平 try/except / if/else 多语句)
ONE_STEP_SCRIPT_TMPL = """\
import os, importlib.util, torch, torch_npu, {lib}
x = torch.randn(2, 3).npu()
y = (x + 1).sum()
sum_v = y.item()
npu_c = torch_npu.npu.device_count()
print("SUM=", sum_v)
print("NPU_COUNT=", npu_c)
if importlib.util.find_spec("wandb") is None:
    print("WANDB_ERR=", "wandb-not-installed")
else:
    import wandb
    _r = wandb.init(mode="offline")
    wandb.log(dict(sum=sum_v, npu_count=npu_c, lib="{lib}"))
    wandb.finish()
    print("WANDB_RUN_ID=", _r.id)
"""


class MinimalResult(TypedDict, total=False):
    """1-step 干跑结果 (D-44, 供 08-04 manifest 写).

    D-45 新增 wandb_run_id: 远程 wandb 离线模式跑出 run.id, 给 sync 阶段定位.
    """
    lib: str
    sum_value: float | None
    npu_count: int | None
    elapsed_ms: int
    exit_code: int
    stdout: str
    stderr: str
    error: str | None
    timeout: bool
    wandb_run_id: str | None  # D-45 远程 wandb run id


def _parse_one_step_output(stdout: str) -> tuple[float | None, int | None, str | None]:
    """解析 stdout 拿 SUM= / NPU_COUNT= / WANDB_RUN_ID=  (D-41 + D-45)."""
    sum_val = None
    npu_count = None
    wandb_run_id = None
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
        elif line.startswith("WANDB_RUN_ID="):
            wandb_run_id = line[len("WANDB_RUN_ID="):].strip()
    return sum_val, npu_count, wandb_run_id


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
    # D-45 决策: 写本地临时脚本 → SFTP 上传到远程 /tmp/one_step_<id>.py → 远程 python 跑
    # 原因: 脚本含 try/except / if/else 多语句, inline python -c 压平会语法错
    import tempfile
    import secrets
    script_id = secrets.token_hex(4)
    local_script = Path(tempfile.gettempdir()) / f"one_step_{script_id}.py"
    local_script.write_text(ONE_STEP_SCRIPT_TMPL.replace("{lib}", lib))
    remote_script = f"/tmp/one_step_{script_id}.py"
    wandb_dir = f"{workdir}/wandb" if workdir else "wandb"
    from workspace_core.ssh.client import SSHClient
    from workspace_core.ssh import HostSpec
    from workspace_core.secrets import resolve_secret
    pw = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    id_file = Path(spec.identity_file).expanduser() if spec.identity_file else None
    host = HostSpec(
        alias=spec.name, host=spec.host, port=spec.port,
        user=spec.user, identity_file=id_file,
    )
    _client = SSHClient(host, bootstrap_password=pw)
    _client.connect(connect_timeout=5.0)
    try:
        sftp = _client.sftp()
        sftp.put(str(local_script), remote_script)
    finally:
        _client.close()
    command = f"mkdir -p {wandb_dir} && WANDB_DIR={wandb_dir} python {remote_script}"
    _pending_cleanup = local_script


    t0 = time.perf_counter()
    try:
        ec, so, se = run_in_env(spec, command, conda_env=conda_env, workdir=workdir, timeout=timeout)
    except CommandTimeoutError as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=True,
            wandb_run_id=None,
        )
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=False,
            wandb_run_id=None,
        )
    elapsed = int((time.perf_counter() - t0) * 1000)
    sum_val, npu_count, wandb_run_id = _parse_one_step_output(so)
    return MinimalResult(
        lib=lib, sum_value=sum_val, npu_count=npu_count, elapsed_ms=elapsed,
        exit_code=ec, stdout=so, stderr=se, error=None, timeout=False,
        wandb_run_id=wandb_run_id,
    )
