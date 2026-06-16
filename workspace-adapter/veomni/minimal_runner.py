"""workspace-adapter.veomni.minimal_runner — veomni 1-step 干跑 (D-44).

复用 Phase 7 D-41 1-step 脚本 (torch_npu + lib).
不引 veomni SDK / 训练脚本, 走 `python -c "..."` 单进程.
"""
from __future__ import annotations
from pathlib import Path

import shlex
import time
from typing import TypedDict

from workspace_core.config import ServerSpec
from workspace_core.ssh import CommandTimeoutError

from ..common.conda_utils import run_in_env
from ..verl.minimal_runner import (
    ONE_STEP_SCRIPT_TMPL,
    MinimalResult,
    _parse_one_step_output,
)


def run_minimal(
    spec: ServerSpec,
    conda_env: str = "",
    workdir: str = "",
    lib: str = "veomni",
    timeout: float = 30.0,
    run_id: str | None = None,
) -> MinimalResult:
    """远程跑 1-step 干跑 (veomni), 返回 MinimalResult (D-44).

    跟 verl runner 同结构, lib 默认 veomni.
    """
    # 用 {lib} 替换 lib 占位; 模板默认 verl, 替换第一次出现
    # D-45 决策: 写本地临时脚本 → SFTP 上传 → 远程 python 跑 (同 verl runner)
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
    remote_log_path = None
    if run_id:
        runs_dir = f"{workdir}/runs" if workdir else "runs"
        remote_log_path = f"{runs_dir}/{run_id}.log"
        command = (
            f"mkdir -p {shlex.quote(wandb_dir)} {shlex.quote(runs_dir)} "
            f"&& : > {shlex.quote(remote_log_path)} "
            f"&& WANDB_DIR={shlex.quote(wandb_dir)} "
            f"python {shlex.quote(remote_script)} 2>&1 | tee -a {shlex.quote(remote_log_path)}"
        )
    else:
        command = (
            f"mkdir -p {shlex.quote(wandb_dir)} "
            f"&& WANDB_DIR={shlex.quote(wandb_dir)} python {shlex.quote(remote_script)}"
        )
    _pending_cleanup = local_script


    t0 = time.perf_counter()
    try:
        ec, so, se = run_in_env(spec, command, conda_env=conda_env, workdir=workdir, timeout=timeout)
    except CommandTimeoutError as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=True,
            wandb_run_id=None, remote_log_path=remote_log_path,
        )
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=False,
            wandb_run_id=None, remote_log_path=remote_log_path,
        )
    elapsed = int((time.perf_counter() - t0) * 1000)
    sum_val, npu_count, wandb_run_id = _parse_one_step_output(so)
    return MinimalResult(
        lib=lib, sum_value=sum_val, npu_count=npu_count, elapsed_ms=elapsed,
        exit_code=ec, stdout=so, stderr=se, error=None, timeout=False,
        wandb_run_id=wandb_run_id, remote_log_path=remote_log_path,
    )
