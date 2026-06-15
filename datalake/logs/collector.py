"""Collect remote 1-step logs into the local AutoResearch run directory."""
from __future__ import annotations

from pathlib import Path

from workspace_core.config import ServerSpec
from workspace_core.secrets import resolve_secret
from workspace_core.ssh import HostSpec, SSHClient, SSHError


DEFAULT_LOCAL_RUNS_ROOT = Path("~/.autoresearch/runs").expanduser()


class LogFetchError(Exception):
    """Remote log fetch failed with a user-readable reason."""


def _resolve_workdir(server: ServerSpec, workdir_override: str | None) -> str:
    if workdir_override:
        return workdir_override
    return getattr(server, "workdir", "/root") or "/root"


def _host_spec(server: ServerSpec) -> HostSpec:
    identity_file = Path(server.identity_file).expanduser() if server.identity_file else None
    return HostSpec(
        alias=server.name,
        host=server.host,
        port=server.port,
        user=server.user,
        identity_file=identity_file,
    )


def collect_log(
    run_id: str,
    server: ServerSpec,
    workdir_override: str | None = None,
    local_runs_root: Path | None = None,
    remote_log_path: str | None = None,
) -> Path:
    """Fetch ``<workdir>/runs/<run_id>.log`` into ``log.txt``.

    The implementation intentionally performs one bounded SFTP read after the
    1-step run. Streaming and inotify-style tailing are left for v1.1.
    """
    if not run_id:
        raise LogFetchError("run_id 不能为空")

    workdir = _resolve_workdir(server, workdir_override)
    remote_path = remote_log_path or f"{workdir}/runs/{run_id}.log"
    root = Path(local_runs_root).expanduser() if local_runs_root else DEFAULT_LOCAL_RUNS_ROOT
    local_dir = root / run_id
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / "log.txt"

    password = (
        resolve_secret(server.bootstrap_password_secret)
        if server.bootstrap_password_secret
        else None
    )
    client = SSHClient(_host_spec(server), bootstrap_password=password)
    try:
        client.connect(connect_timeout=5.0)
        sftp = client.sftp()
        try:
            remote_file = sftp.open(remote_path, "rb")
        except FileNotFoundError as exc:
            raise LogFetchError(f"远程日志不存在: {remote_path}") from exc
        except PermissionError as exc:
            raise LogFetchError(f"无权限读取远程日志: {remote_path}") from exc
        except OSError as exc:
            raise LogFetchError(f"无法打开远程日志 {remote_path}: {exc}") from exc

        try:
            prefetch = getattr(remote_file, "prefetch", None)
            if callable(prefetch):
                prefetch()
            with local_path.open("wb") as out:
                while True:
                    chunk = remote_file.read(1024 * 128)
                    if not chunk:
                        break
                    if isinstance(chunk, str):
                        chunk = chunk.encode("utf-8")
                    out.write(chunk)
        finally:
            close = getattr(remote_file, "close", None)
            if callable(close):
                close()
    except LogFetchError:
        raise
    except SSHError as exc:
        raise LogFetchError(f"SSH 拉取日志失败: {exc}") from exc
    except OSError as exc:
        raise LogFetchError(f"SFTP 拉取日志失败: {exc}") from exc
    finally:
        client.close()

    return local_path


def tail_remote_log(
    server: ServerSpec,
    remote_log_path: str,
    run_id: str | None = None,
    local_runs_root: Path | None = None,
) -> Path:
    """Compatibility wrapper for callers that already know the remote path."""
    resolved_run_id = run_id or Path(remote_log_path).stem
    return collect_log(
        resolved_run_id,
        server,
        local_runs_root=local_runs_root,
        remote_log_path=remote_log_path,
    )
