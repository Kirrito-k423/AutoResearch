"""workspace-adapter.common.conda_utils — 共享 SSH + conda 工具 (D-44).

复用 workspace_core.ssh.SSHClient, 单次干净执行 `conda run -n <env>` 命令.
不引第三方客户端 (D-39 决策).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
from workspace_core.config import ServerSpec
from workspace_core.ssh import (
    AuthError,
    BootstrapFailed,
    CommandTimeoutError,
    HostSpec,
    SSHClient,
    SSHError,
)
from workspace_core.secrets import resolve_secret


# === Constants ===

ONE_STEP_TIMEOUT_S: float = 30.0  # D-41: 1-step 走 30s


def _host_spec(spec: ServerSpec) -> HostSpec:
    id_file = None
    if spec.identity_file:
        id_file = Path(spec.identity_file).expanduser()
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
    timeout: float = ONE_STEP_TIMEOUT_S,
) -> tuple[int, str, str]:
    """跑远程命令, 返回 (exit_code, stdout, stderr)."""
    pw = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    client = SSHClient(_host_spec(spec), bootstrap_password=pw)
    try:
        client.connect(connect_timeout=5.0)
    except (AuthError, SSHError) as e:
        raise BootstrapFailed(f"SSH 连接失败: {e}") from e
    try:
        return client.exec(command, timeout=timeout)
    finally:
        client.close()


def _ssh_exec_capture_until_marker(
    spec: ServerSpec,
    command: str,
    *,
    marker: str,
    timeout: float = ONE_STEP_TIMEOUT_S,
    grace_period: float = 0.2,
) -> tuple[int, str, str]:
    """跑远程命令; 读到 marker 后主动收口 channel."""
    pw = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    client = SSHClient(_host_spec(spec), bootstrap_password=pw)
    try:
        client.connect(connect_timeout=5.0)
    except (AuthError, SSHError) as e:
        raise BootstrapFailed(f"SSH 连接失败: {e}") from e
    try:
        return client.exec_until_marker(
            command,
            marker=marker,
            timeout=timeout,
            grace_period=grace_period,
        )
    finally:
        client.close()


def build_conda_command(conda_env: str, command: str) -> str:
    """拼 `conda run -n <env> <command>` 或直通 (无 env 时).

    D-40: 单次 conda run, 不 activate.
    D-44: 不引 framework SDK, 走 `python -c "<inline>"`
    """
    if not conda_env:
        return command
    # conda run -n <env> <command>;  不加 --no-capture-output 避免吞 stderr
    return f"conda run -n {conda_env} {command}"


def build_cd_command(workdir: str, command: str) -> str:
    """拼 `cd <workdir> && <command>` (D-46 workdir 字段).

    workdir 为空时直通. 不引 ssh 客户端状态变化.
    """
    if not workdir:
        return command
    # 单引号包裹避免路径含空格 / 特殊字符
    safe_dir = workdir.replace("'", "'\\''")
    return f"cd '{safe_dir}' && {command}"


def run_in_env(
    spec: ServerSpec,
    command: str,
    conda_env: str = "",
    workdir: str = "",
    timeout: float = ONE_STEP_TIMEOUT_S,
) -> tuple[int, str, str]:
    """远程跑命令, 自动套 `cd <workdir> && conda run -n <env> <cmd>` (D-44, D-46).

    复用 Phase 7 _ssh_exec_capture 模式.
    """
    env_cmd = build_conda_command(conda_env, command) if conda_env else command
    full_cmd = build_cd_command(workdir, env_cmd)
    return _ssh_exec_capture(spec, full_cmd, timeout=timeout)


def run_in_env_until_marker(
    spec: ServerSpec,
    command: str,
    *,
    marker: str,
    conda_env: str = "",
    workdir: str = "",
    timeout: float = ONE_STEP_TIMEOUT_S,
    grace_period: float = 0.2,
) -> tuple[int, str, str]:
    """远程跑命令; 一旦输出出现 marker 就主动结束本地等待."""
    env_cmd = build_conda_command(conda_env, command) if conda_env else command
    full_cmd = build_cd_command(workdir, env_cmd)
    return _ssh_exec_capture_until_marker(
        spec,
        full_cmd,
        marker=marker,
        timeout=timeout,
        grace_period=grace_period,
    )
