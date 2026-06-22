"""Stage local dependency sources onto the remote host for formal Verl runs."""
from __future__ import annotations

import shlex
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

from workspace_core.config import ServerSpec
from workspace_core.secrets import resolve_secret
from workspace_core.ssh import HostSpec
from workspace_core.ssh.client import SSHClient


REPO_MOUNT_PATHS: dict[str, str] = {
    "verl": "/verl",
    "vllm": "/vllm",
    "transformers": "/transformers",
    "mindspeed": "/mindspeed",
    "veomni": "/veomni",
}

_SKIP_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}
_SKIP_SUFFIXES = {".pyc", ".pyo"}


class DependencySourceSyncError(RuntimeError):
    """Raised when a configured dependency repo cannot be staged remotely."""


def filter_dependency_repo_paths(
    *,
    dependency_repo_paths: dict[str, str] | None,
    server: str,
    model_id: str,
    execution_profile: str | None = None,
) -> dict[str, str]:
    """Return the dependency repos that should be mounted for this execution profile."""
    configured = dict(dependency_repo_paths or {})
    profile = (execution_profile or "fsdp").strip().lower()
    if profile == "auto":
        profile = "fsdp"
    if profile == "veomni":
        configured.pop("vllm", None)
    return configured


def stage_dependency_sources(
    spec: ServerSpec,
    *,
    run_id: str,
    remote_workdir: str,
    dependency_repo_paths: dict[str, str] | None,
) -> dict[str, str]:
    """Upload configured source repos and return container_path -> remote_path mounts."""
    configured = dict(dependency_repo_paths or {})
    if not configured:
        return {}

    id_file = Path(spec.identity_file).expanduser() if spec.identity_file else None
    password = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    host = HostSpec(
        alias=spec.name,
        host=spec.host,
        port=spec.port,
        user=spec.user,
        identity_file=id_file,
    )
    remote_root = PurePosixPath(remote_workdir) / "autoresearch" / "runs" / run_id / "deps"
    mounts: dict[str, str] = {}
    with SSHClient(host, bootstrap_password=password) as client:
        _ensure_remote_dir(client, remote_root)
        sftp = client.sftp()
        try:
            for repo_name, raw_path in configured.items():
                if repo_name not in REPO_MOUNT_PATHS:
                    supported = ", ".join(sorted(REPO_MOUNT_PATHS))
                    raise DependencySourceSyncError(
                        f"unsupported dependency repo '{repo_name}', supported: {supported}"
                    )
                local_path = Path(raw_path).expanduser()
                if not local_path.exists() or not local_path.is_dir():
                    raise DependencySourceSyncError(
                        f"dependency repo path missing: {repo_name}={local_path}"
                    )
                container_path = _container_mount_path(repo_name, local_path)
                remote_repo_dir = remote_root / repo_name
                _sync_repo_archive(
                    client,
                    sftp=sftp,
                    repo_name=repo_name,
                    local_path=local_path,
                    remote_repo_dir=remote_repo_dir,
                )
                mounts[container_path] = remote_repo_dir.as_posix()
        finally:
            sftp.close()
    return mounts


def _ensure_remote_dir(client: SSHClient, remote_dir: PurePosixPath) -> None:
    command = f"mkdir -p {shlex.quote(remote_dir.as_posix())}"
    code, stdout, stderr = client.exec(command, timeout=30.0)
    if code != 0:
        detail = (stderr or stdout or "").strip() or f"exit={code}"
        raise DependencySourceSyncError(f"failed to create remote dir {remote_dir}: {detail}")


def _sync_repo_archive(
    client: SSHClient,
    *,
    sftp,
    repo_name: str,
    local_path: Path,
    remote_repo_dir: PurePosixPath,
) -> None:
    local_archive = _build_repo_archive(local_path)
    remote_archive = PurePosixPath("/tmp") / f"autoresearch-{repo_name}-{local_archive.name}"
    try:
        sftp.put(str(local_archive), remote_archive.as_posix())
        command = " && ".join(
            [
                f"rm -rf {shlex.quote(remote_repo_dir.as_posix())}",
                f"mkdir -p {shlex.quote(remote_repo_dir.as_posix())}",
                f"tar -xzf {shlex.quote(remote_archive.as_posix())} -C {shlex.quote(remote_repo_dir.as_posix())} --strip-components 1",
                f"rm -f {shlex.quote(remote_archive.as_posix())}",
            ]
        )
        code, stdout, stderr = client.exec(command, timeout=300.0)
        if code != 0:
            detail = (stderr or stdout or "").strip() or f"exit={code}"
            raise DependencySourceSyncError(f"failed to unpack {repo_name}: {detail}")
    finally:
        local_archive.unlink(missing_ok=True)


def _build_repo_archive(local_path: Path) -> Path:
    fd, raw_path = tempfile.mkstemp(prefix=f"{local_path.name}-", suffix=".tar.gz")
    Path(raw_path).unlink(missing_ok=True)
    archive_path = Path(raw_path)

    def _filter(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
        rel_parts = Path(info.name).parts[1:]
        if any(part in _SKIP_PARTS for part in rel_parts):
            return None
        if rel_parts and Path(rel_parts[-1]).suffix in _SKIP_SUFFIXES:
            return None
        return info

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(str(local_path), arcname=local_path.name, filter=_filter)
    return archive_path


def _container_mount_path(repo_name: str, local_path: Path) -> str:
    if repo_name == "transformers":
        package_root = local_path / "utils" / "generic.py"
        repo_root = local_path / "src" / "transformers"
        if package_root.exists() and not repo_root.exists():
            return "/transformers/src/transformers"
    return REPO_MOUNT_PATHS[repo_name]
