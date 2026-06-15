"""datalake.wandb.sync — 远程 wandb 离线 run → 本地 sync (D-45).

`sync_run(run_id, spec, workdir)`:
  1. 远程验 wandb/<run_id> 目录存在 (调 `ls <workdir>/wandb/ | grep <run_id>`)
  2. SFTP 拉整个目录到 `~/.autoresearch/runs/<run_id>/wandb/`
  3. 本地 `wandb sync <local_path>` subprocess 调本地 wandb 服务
  4. 失败 → 4 类异常 (WandbNotInstalled / NoLocalServer / NoRemoteRun / SyncFailed)
"""
from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from workspace_core.config import ServerSpec
from verl_workspace_adapter.common.conda_utils import _ssh_exec_capture


# === Exceptions (D-45: 4 类错误诊断) ===

class WandbSyncError(Exception):
    """wandb sync 失败的基类."""


class WandbNotInstalled(WandbSyncError):
    """Mac 本地没装 wandb CLI."""


class NoLocalServer(WandbSyncError):
    """本地 wandb 服务没起 (Phase 1 docker 容器)."""


class NoRemoteRun(WandbSyncError):
    """远程 wandb/<run_id> 目录不存在."""


class SyncFailed(WandbSyncError):
    """wandb sync 进程失败."""


# === Constants ===

DEFAULT_LOCAL_RUNS_ROOT = Path("~/.autoresearch/runs").expanduser()
WANDB_SYNC_TIMEOUT_S: float = 30.0
REMOTE_LS_TIMEOUT_S: float = 10.0


def _list_remote_wandb_runs(spec: ServerSpec, workdir: str, run_id_prefix: str = "") -> list[str]:
    """远程 `ls <workdir>/wandb/` 拿 run 目录名列表.

    Returns: run 目录名列表 (e.g. ['run-20260615_050749-abc123'])
    """
    # wandb SDK 写到 <WANDB_DIR>/wandb/offline-run-<ts>-<id>/
    # (D-45 runner 设 WANDB_DIR=/root/wandb, 实际跑在 /root/wandb/wandb/)
    wandb_runs_dir = f"{workdir}/wandb/wandb" if workdir else "wandb/wandb"
    cmd = f"ls -1 {wandb_runs_dir}/ 2>/dev/null | grep -E '(offline-)?run-' | head -20"
    ec, so, se = _ssh_exec_capture(spec, cmd, timeout=REMOTE_LS_TIMEOUT_S)
    if ec != 0 and not so.strip():
        return []
    runs = [line.strip() for line in so.splitlines() if line.strip().startswith(("offline-run-", "run-"))]
    if run_id_prefix:
        runs = [r for r in runs if run_id_prefix in r]
    return runs


def _sftp_fetch_dir(spec: ServerSpec, remote_dir: str, local_dir: Path) -> None:
    """SFTP 递归拉远程目录到本地.

    用 paramiko SFTP 走 .from_transport, 不引第三方 (D-39).
    """
    from pathlib import Path as _P
    from workspace_core.ssh.client import SSHClient
    from workspace_core.ssh import HostSpec
    from workspace_core.secrets import resolve_secret

    local_dir = _P(local_dir)
    local_dir.mkdir(parents=True, exist_ok=True)

    pw = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    id_file = Path(spec.identity_file).expanduser() if spec.identity_file else None
    host = HostSpec(
        alias=spec.name,
        host=spec.host,
        port=spec.port,
        user=spec.user,
        identity_file=id_file,
    )
    client = SSHClient(host, bootstrap_password=pw)
    client.connect(connect_timeout=5.0)
    try:
        sftp = client.sftp()
        # SFTP 没原生 recursive, 自己走
        _sftp_walk(sftp, remote_dir, str(local_dir))
    finally:
        client.close()


def _sftp_walk(sftp, remote_dir: str, local_dir: str) -> None:
    """递归 SFTP 拉目录. 跳过 .wandb / .tmp / wandb-summary.json (sync 阶段重新生成)."""
    from pathlib import Path as _P
    SKIP_SUFFIX = (".tmp", ".partial", ".lock")
    local_p = _P(local_dir)
    local_p.mkdir(parents=True, exist_ok=True)
    try:
        items = sftp.listdir_attr(remote_dir)
    except IOError:
        return
    for item in items:
        remote_path = f"{remote_dir}/{item.filename}"
        local_path = local_p / item.filename
        if item.filename.startswith(".") or item.filename.endswith(SKIP_SUFFIX):
            continue
        if item.st_mode is not None and (item.st_mode & 0o170000) == 0o040000:  # dir
            _sftp_walk(sftp, remote_path, str(local_path))
        else:
            try:
                sftp.get(remote_path, str(local_path))
            except IOError:
                pass  # 跳过无法读的文件


def _check_wandb_cli() -> None:
    """Mac 本地验 `wandb` CLI 装没装."""
    if shutil.which("wandb") is None:
        raise WandbNotInstalled(
            "Mac 本地没装 wandb CLI; 装: pip install wandb"
        )


def _check_local_wandb_server(url: str = "http://localhost:8080/health") -> bool:
    """快速 check 本地 wandb 服务在不在 (Phase 1 docker 容器, port 8080).

    用 curl / -m 2 短 timeout; 不引 requests 硬 dep.
    """
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _wandb_sync_subprocess(local_path: Path, timeout: float = WANDB_SYNC_TIMEOUT_S) -> tuple[int, str, str]:
    """本地 `wandb sync <path>` 调本地 wandb 服务."""
    # wandb 0.27.x 删了 --no-videos
    # env WANDB_BASE_URL 让 sync 走本地服务 (Phase 1 SVC-02 起的 8080 容器)
    # 缺省 https://api.wandb.ai (云端), 需 wandb login
    import os
    env = os.environ.copy()
    # 用户没设 WANDB_BASE_URL 时默认走 http://localhost:8080 (本地服务)
    env.setdefault("WANDB_BASE_URL", "http://localhost:8080")
    proc = subprocess.run(
        ["wandb", "sync", str(local_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


# === Public API ===

def sync_run(
    run_id: str,
    spec: ServerSpec,
    workdir: str = "",
    local_runs_root: Path | None = None,
) -> Path:
    """把远程 wandb 离线 run 拉回本地 + 调 wandb sync 导入 (D-45).

    Args:
        run_id: 远程 wandb run id (e.g. "abc123" 或 run 目录名 "run-<ts>-<id>")
                支持 prefix 模式: 传短 id 也能匹配 (找最长 prefix 的 run)
        spec: ServerSpec, SSH 凭据
        workdir: 远程工作目录 (D-46, 默认 '/root' 走 getattr 兜底)
        local_runs_root: 本地 runs 根目录, 默认 ~/.autoresearch/runs

    Returns:
        本地 wandb 目录路径 (Path)

    Raises:
        WandbNotInstalled: Mac 本地没装 wandb CLI
        NoRemoteRun: 远程 wandb/<run_id> 不存在
        SyncFailed: wandb sync 进程失败
    """
    if not workdir:
        workdir = "/root"
    if local_runs_root is None:
        local_runs_root = DEFAULT_LOCAL_RUNS_ROOT
    local_runs_root = Path(local_runs_root).expanduser()

    # 1. 本地前置检查
    _check_wandb_cli()
    # 注意: 本地 wandb 服务 check 不阻塞 (D-45 graceful), sync 阶段才知道

    # 2. 远程 ls wandb/ 找 run 目录
    remote_runs = _list_remote_wandb_runs(spec, workdir, run_id_prefix=run_id)
    if not remote_runs:
        raise NoRemoteRun(
            f"远程 {workdir}/wandb/ 下找不到含 '{run_id}' 的 run 目录; "
            f"1-step 跑了 wandb.init 才会写"
        )
    # 选最长的 (完整 run id 通常最 specific)
    remote_run = max(remote_runs, key=len)
    remote_dir = f"{workdir}/wandb/wandb/{remote_run}"

    # 3. SFTP 拉回本地
    local_run_dir = local_runs_root / run_id / "wandb"
    if local_run_dir.exists():
        shutil.rmtree(local_run_dir)
    _sftp_fetch_dir(spec, remote_dir, local_run_dir)

    # 4. 本地 wandb sync
    ec, so, se = _wandb_sync_subprocess(local_run_dir)
    if ec != 0:
        # wandb sync 失败不一定是 CLI 错, 也可能是服务没起
        # 给可读错误 + 提示启服务
        if "Unable to connect" in se or "Connection refused" in se:
            raise SyncFailed(
                f"wandb sync 失败: 本地 wandb 服务没起? `autoresearch services start`; "
                f"stderr={se.strip()[:200]}"
            )
        raise SyncFailed(
            f"wandb sync 失败 exit={ec}; "
            f"stdout={so.strip()[:200]}; stderr={se.strip()[:200]}"
        )

    return local_run_dir
