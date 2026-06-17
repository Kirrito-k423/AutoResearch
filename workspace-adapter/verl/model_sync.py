"""Local model cache preparation and remote staging for formal Verl runs."""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

from pydantic import BaseModel
import requests

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
HF_ENV_DEFAULTS = {
    "HF_XET_HIGH_PERFORMANCE": "1",
}
MODEL_ALLOW_PATTERNS = (
    "*.json",
    "*.safetensors",
    "*.txt",
    "*.model",
    "*.tiktoken",
    "*.jinja",
)
MODEL_FILE = "model.safetensors"
MODEL_INDEX_FILE = "model.safetensors.index.json"
_SIDECAR_FILES = {
    "chat_template.json",
    "config.json",
    "generation_config.json",
    "merges.txt",
    "preprocessor_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "video_preprocessor_config.json",
    "vocab.json",
}
_RESUME_METADATA_FILES = {
    "config.json",
    MODEL_INDEX_FILE,
}


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
    if _resume_metadata_ready(model_cache) and _largest_incomplete(model_cache) is not None:
        try:
            _resume_model_download(config.model_id, model_cache, proxy_url=proxy_url)
        except Exception:
            pass
        else:
            return PreparedModelCache(
                model_id=config.model_id,
                cache_root=root,
                model_cache=model_cache,
                ready=True,
                downloaded=True,
            )

    previous_env = {
        key: os.environ.get(key)
        for key in (*PROXY_ENV_KEYS, *HF_ENV_DEFAULTS.keys(), "HF_HUB_DISABLE_XET")
    }
    if proxy_url:
        for key in PROXY_ENV_KEYS:
            os.environ[key] = proxy_url
        os.environ["HF_HUB_DISABLE_XET"] = "1"
    else:
        for key, value in HF_ENV_DEFAULTS.items():
            os.environ.setdefault(key, value)
    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise ModelCacheError(
            "缺少 huggingface_hub，无法准备 formal case 本地模型缓存。请先执行 `uv sync`。"
        ) from exc
    try:
        kwargs = {
            "repo_id": config.model_id,
            "local_dir": str(model_cache),
            "allow_patterns": list(MODEL_ALLOW_PATTERNS),
        }
        snapshot_download(**kwargs)
    except Exception as exc:
        _resume_or_raise(
            config.model_id,
            model_cache,
            proxy_url=proxy_url,
            initial_error=exc,
            context="下载模型缓存失败",
        )
    finally:
        for key, value in previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    if not _model_ready(model_cache):
        _resume_or_raise(
            config.model_id,
            model_cache,
            proxy_url=proxy_url,
            context=f"模型缓存不完整: {model_cache}",
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
    if not (model_cache / "config.json").exists():
        return False
    if (model_cache / MODEL_FILE).exists():
        return True

    shard_names = _indexed_weight_files(model_cache)
    if not shard_names:
        return False
    return all((model_cache / name).exists() for name in shard_names)


def _sidecars_ready(model_cache: Path) -> bool:
    return all((model_cache / name).exists() for name in _SIDECAR_FILES)


def _resume_metadata_ready(model_cache: Path) -> bool:
    return all((model_cache / name).exists() for name in _RESUME_METADATA_FILES)


def _resume_or_raise(
    model_id: str,
    model_cache: Path,
    *,
    proxy_url: str | None,
    context: str,
    initial_error: Exception | None = None,
) -> None:
    if not _resume_metadata_ready(model_cache):
        detail = f"{context}: {model_id}" if initial_error else context
        if initial_error is None:
            raise ModelCacheError(f"{detail}，缺少续传所需的关键 metadata 文件。")
        raise ModelCacheError(f"{detail}: {initial_error}") from initial_error

    try:
        _resume_model_download(model_id, model_cache, proxy_url=proxy_url)
    except Exception as resume_exc:
        if initial_error is None:
            raise ModelCacheError(f"{context}；单文件续传也失败: {resume_exc}") from resume_exc
        raise ModelCacheError(
            f"{context}: {model_id}: {initial_error}; 单文件续传也失败: {resume_exc}"
        ) from resume_exc

    if not _model_ready(model_cache):
        raise ModelCacheError(f"{context}，单文件续传结束后仍缺少 config.json 或 safetensors 权重。")


def _resume_model_download(
    model_id: str,
    model_cache: Path,
    *,
    proxy_url: str | None,
) -> None:
    incomplete_path = _largest_incomplete(model_cache)
    if incomplete_path is None:
        raise ModelCacheError(f"未找到可续传的中间文件: {model_cache}")
    target_name = _resume_target_name(model_cache, incomplete_path)

    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    session = requests.Session()
    resolve_url = f"https://huggingface.co/{model_id}/resolve/main/{target_name}"
    retries = 0
    total_size = 0
    while True:
        current_size = incomplete_path.stat().st_size
        download_url, total_size = _resolve_download_url(session, resolve_url, proxies)
        if total_size and current_size >= total_size:
            break

        headers = {"Range": f"bytes={current_size}-"} if current_size else {}
        try:
            response = session.get(
                download_url,
                headers=headers,
                stream=True,
                proxies=proxies,
                timeout=(30, 300),
            )
            response.raise_for_status()
            if current_size and response.status_code == 200:
                raise ModelCacheError("直链未接受 Range 续传请求。")
            with response:
                with incomplete_path.open("ab" if current_size else "wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
        except requests.RequestException as exc:
            retries += 1
            latest_size = incomplete_path.stat().st_size
            if total_size and latest_size >= total_size:
                break
            if proxy_url and latest_size > current_size:
                _resume_via_curl(
                    resolve_url=resolve_url,
                    incomplete_path=incomplete_path,
                    proxy_url=proxy_url,
                    expected_size=total_size,
                )
                break
            if retries >= 8:
                raise ModelCacheError(
                    f"单文件续传多次中断仍未完成: got={latest_size}, want={total_size}, last_error={exc}"
                ) from exc
            continue

        latest_size = incomplete_path.stat().st_size
        if not total_size or latest_size >= total_size:
            break

    final_size = incomplete_path.stat().st_size
    if total_size and final_size != total_size:
        raise ModelCacheError(
            f"单文件续传后模型大小不匹配: got={final_size}, want={total_size}"
        )

    final_path = model_cache / target_name
    incomplete_path.replace(final_path)
    for candidate in model_cache.rglob("*.incomplete"):
        candidate.unlink(missing_ok=True)


def _resolve_download_url(
    session: requests.Session,
    resolve_url: str,
    proxies: dict[str, str] | None,
) -> tuple[str, int]:
    last_error: Exception | None = None
    for _ in range(3):
        try:
            response = session.get(
                resolve_url,
                allow_redirects=False,
                proxies=proxies,
                timeout=(30, 120),
            )
            response.raise_for_status()
            location = response.headers.get("location") or resolve_url
            total_size = int(
                response.headers.get("x-linked-size")
                or response.headers.get("Content-Length")
                or 0
            )
            return location, total_size
        except requests.RequestException as exc:
            last_error = exc
    raise ModelCacheError(f"获取模型直链失败: {last_error}")


def _resume_via_curl(
    *,
    resolve_url: str,
    incomplete_path: Path,
    proxy_url: str | None,
    expected_size: int,
) -> None:
    command = [
        "curl",
        "-L",
        "--fail",
        "--retry",
        "8",
        "--retry-all-errors",
        "--connect-timeout",
        "30",
        "--continue-at",
        "-",
        "--output",
        str(incomplete_path),
        resolve_url,
    ]
    if proxy_url:
        command[1:1] = ["--proxy", proxy_url]
    try:
        proc = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ModelCacheError("requests 续传中断后尝试 curl 兜底失败: 本机未找到 curl") from exc

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise ModelCacheError(f"curl 续传失败: {detail or f'exit={proc.returncode}'}")

    final_size = incomplete_path.stat().st_size
    if expected_size and final_size < expected_size:
        raise ModelCacheError(
            f"curl 续传结束后模型大小仍不完整: got={final_size}, want={expected_size}"
        )


def _largest_incomplete(model_cache: Path) -> Path | None:
    candidates = sorted(
        model_cache.rglob("*.incomplete"),
        key=lambda item: item.stat().st_size,
        reverse=True,
    )
    return candidates[0] if candidates else None


def _indexed_weight_files(model_cache: Path) -> list[str]:
    index_path = model_cache / MODEL_INDEX_FILE
    if not index_path.exists():
        return []
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return []
    weight_map = payload.get("weight_map")
    if not isinstance(weight_map, dict):
        return []
    # Preserve order but drop duplicates.
    return list(dict.fromkeys(str(name) for name in weight_map.values() if name))


def _resume_target_name(model_cache: Path, incomplete_path: Path) -> str:
    shard_names = _indexed_weight_files(model_cache)
    if len(shard_names) == 1:
        return shard_names[0]
    incomplete_name = incomplete_path.name.removesuffix(".incomplete")
    if incomplete_name and incomplete_name != incomplete_path.name:
        return incomplete_name
    return MODEL_FILE


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
