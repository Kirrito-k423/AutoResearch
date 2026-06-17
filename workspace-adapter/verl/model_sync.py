"""Local model cache preparation and remote staging for formal Verl runs."""
from __future__ import annotations

import os
import shlex
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

from pydantic import BaseModel

from workspace_core.config import ServerSpec
from workspace_core.secrets import resolve_secret
from workspace_core.ssh import HostSpec
from workspace_core.ssh.client import SSHClient

from .case_config import VerlCaseConfig


PROXY_ENV_KEYS = (
    "http_proxy",
    "https_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
)
MODEL_ALLOW_PATTERNS = (
    "*.json",
    "*.safetensors",
    "*.txt",
    "*.model",
    "*.tiktoken",
    "*.jinja",
)


class ModelCacheError(RuntimeError):
    """Raised when the local formal-case model cache cannot be prepared."""


class ModelSyncError(RuntimeError):
    """Raised when the prepared local model cache cannot be staged remotely."""


class PreparedModelCache(BaseModel):
    """Local model cache metadata kept with the immutable run config."""

    model_id: str
    cache_root: Path
    model_cache: Path
    ready: bool
    downloaded: bool = False


def prepare_model_cache(
    config: VerlCaseConfig,
    cache_root: str | Path,
    *,
    proxy_url: str | None = None,
) -> PreparedModelCache:
    """Ensure the formal-case model exists under the configured local cache root."""
    root = Path(cache_root).expanduser()
    model_cache = root / "models" / config.model_id.replace("/", "__")
    model_cache.mkdir(parents=True, exist_ok=True)
    if _model_ready(model_cache):
        return PreparedModelCache(
            model_id=config.model_id,
            cache_root=root,
            model_cache=model_cache,
            ready=True,
            downloaded=False,
        )

    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise ModelCacheError(
            "缺少 huggingface_hub，无法准备 formal case 本地模型缓存。请先执行 `uv sync`。"
        ) from exc

    previous_env = {key: os.environ.get(key) for key in PROXY_ENV_KEYS}
    if proxy_url:
        for key in PROXY_ENV_KEYS:
            os.environ[key] = proxy_url
    try:
        kwargs = {
            "repo_id": config.model_id,
            "local_dir": str(model_cache),
            "allow_patterns": list(MODEL_ALLOW_PATTERNS),
        }
        try:
            snapshot_download(local_dir_use_symlinks=False, **kwargs)
        except TypeError:
            snapshot_download(**kwargs)
    except Exception as exc:
        raise ModelCacheError(f"下载模型缓存失败: {config.model_id}: {exc}") from exc
    finally:
        for key, value in previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    if not _model_ready(model_cache):
        raise ModelCacheError(
            f"模型缓存不完整: {model_cache}，缺少 config.json 或 safetensors 权重。"
        )
    return PreparedModelCache(
        model_id=config.model_id,
        cache_root=root,
        model_cache=model_cache,
        ready=True,
        downloaded=True,
    )


def stage_model_cache(
    spec: ServerSpec,
    *,
    local_model_dir: str | Path,
    remote_model_dir: str | PurePosixPath,
) -> str:
    """Upload the prepared local model cache into the current remote run directory."""
    local_path = Path(local_model_dir).expanduser()
    if not _model_ready(local_path):
        raise ModelSyncError(f"本地模型缓存不可用: {local_path}")

    id_file = Path(spec.identity_file).expanduser() if spec.identity_file else None
    password = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    host = HostSpec(
        alias=spec.name,
        host=spec.host,
        port=spec.port,
        user=spec.user,
        identity_file=id_file,
    )
    remote_dir = PurePosixPath(str(remote_model_dir))
    with SSHClient(host, bootstrap_password=password) as client:
        _ensure_remote_dir(client, remote_dir.parent)
        archive = _build_model_archive(local_path)
        remote_archive = PurePosixPath("/tmp") / archive.name
        sftp = client.sftp()
        try:
            sftp.put(str(archive), remote_archive.as_posix())
        finally:
            sftp.close()
            archive.unlink(missing_ok=True)
        command = " && ".join(
            [
                f"rm -rf {shlex.quote(remote_dir.as_posix())}",
                f"mkdir -p {shlex.quote(remote_dir.as_posix())}",
                f"tar -xf {shlex.quote(remote_archive.as_posix())} -C {shlex.quote(remote_dir.as_posix())} --strip-components 1",
                f"rm -f {shlex.quote(remote_archive.as_posix())}",
            ]
        )
        code, stdout, stderr = client.exec(command, timeout=3600.0)
        if code != 0:
            detail = (stderr or stdout or "").strip() or f"exit={code}"
            raise ModelSyncError(f"远端模型缓存同步失败: {detail}")
    return remote_dir.as_posix()


def _model_ready(model_cache: Path) -> bool:
    return (model_cache / "config.json").exists() and any(model_cache.glob("*.safetensors"))


def _ensure_remote_dir(client: SSHClient, remote_dir: PurePosixPath) -> None:
    command = f"mkdir -p {shlex.quote(remote_dir.as_posix())}"
    code, stdout, stderr = client.exec(command, timeout=30.0)
    if code != 0:
        detail = (stderr or stdout or "").strip() or f"exit={code}"
        raise ModelSyncError(f"远端目录创建失败 {remote_dir}: {detail}")


def _build_model_archive(local_path: Path) -> Path:
    fd, raw_path = tempfile.mkstemp(prefix=f"{local_path.name}-", suffix=".tar")
    os.close(fd)
    archive_path = Path(raw_path)
    archive_path.unlink(missing_ok=True)
    with tarfile.open(archive_path, "w") as tar:
        tar.add(str(local_path), arcname=local_path.name)
    return archive_path
