"""Model and dataset asset registry helpers.

The registry is intentionally YAML-shaped and conservative: it records where
asset bytes live, but never stores credentials.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import yaml


AssetKind = Literal["model", "dataset"]

DEFAULT_DATA_PATH = Path("config/data.yaml")
DEFAULT_TEMPLATE_PATH = Path("config/data.example.yaml")
_KIND_BUCKETS: dict[AssetKind, str] = {"model": "models", "dataset": "datasets"}


class AssetRegistryError(RuntimeError):
    """Raised when the asset registry cannot be read or updated."""


def asset_cache_dir(cache_root: str | Path, kind: AssetKind, canonical_id: str) -> Path:
    """Return the conventional local cache directory for an asset."""
    bucket = _KIND_BUCKETS[kind]
    return Path(cache_root).expanduser() / bucket / _asset_dir_name(canonical_id)


def load_registry(path: str | Path | None = None) -> dict[str, Any]:
    """Load `config/data.yaml`, falling back to the tracked example if absent."""
    registry_path = Path(path).expanduser() if path is not None else DEFAULT_DATA_PATH
    if registry_path.exists():
        return _read_yaml(registry_path)
    sibling_template = registry_path.with_name("data.example.yaml")
    if sibling_template.exists():
        return _read_yaml(sibling_template)
    if path is None and DEFAULT_TEMPLATE_PATH.exists():
        return _read_yaml(DEFAULT_TEMPLATE_PATH)
    raise AssetRegistryError(f"资产登记簿不存在: {registry_path}")


def write_registry(registry: dict[str, Any], path: str | Path | None = None) -> None:
    """Persist registry YAML to `path` or `config/data.yaml`."""
    registry_path = Path(path).expanduser() if path is not None else DEFAULT_DATA_PATH
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(
        registry,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    registry_path.write_text(text, encoding="utf-8")


def find_asset(
    registry: dict[str, Any],
    *,
    kind: AssetKind,
    canonical_id: str,
) -> tuple[str, dict[str, Any]] | None:
    """Find an asset by canonical id inside a loaded registry."""
    bucket = _asset_bucket(registry, kind, create=False)
    for key, value in bucket.items():
        if isinstance(value, dict) and value.get("canonical_id") == canonical_id:
            return key, value
    return None


def remote_locations_for_asset(entry: dict[str, Any]) -> list[dict[str, str]]:
    """Return all remote locations recorded for one asset.

    `remote` is the legacy single-location shape. `remotes` is the preferred
    multi-host shape keyed by server name, but a list is accepted for tolerance.
    """
    locations: list[dict[str, str]] = []

    remotes = entry.get("remotes")
    if isinstance(remotes, dict):
        for key, value in remotes.items():
            if not isinstance(value, dict):
                continue
            location = _remote_location(value, fallback_server=str(key))
            if location is not None:
                locations.append(location)
    elif isinstance(remotes, list):
        for value in remotes:
            if not isinstance(value, dict):
                continue
            location = _remote_location(value)
            if location is not None:
                locations.append(location)

    remote = entry.get("remote")
    if isinstance(remote, dict):
        location = _remote_location(remote)
        if location is not None:
            marker = (
                location.get("server", ""),
                location.get("host", ""),
                location.get("path", ""),
            )
            seen = {
                (
                    item.get("server", ""),
                    item.get("host", ""),
                    item.get("path", ""),
                )
                for item in locations
            }
            if marker not in seen:
                locations.append(location)

    return locations


def select_remote_location(
    entry: dict[str, Any],
    *,
    server_name: str | None = None,
    host: str | None = None,
) -> dict[str, str] | None:
    """Select the best remote location for a server from an asset entry."""
    locations = remote_locations_for_asset(entry)
    if server_name:
        for location in locations:
            if location.get("server") == server_name:
                return location
    if host:
        for location in locations:
            if location.get("host") == host:
                return location
    for location in locations:
        if not location.get("server") and not location.get("host"):
            return location
    return None


def local_path_for_asset(
    *,
    kind: AssetKind,
    canonical_id: str,
    cache_root: str | Path,
    data_config_path: str | Path | None = None,
) -> Path:
    """Resolve the preferred local path from registry, falling back to convention."""
    if data_config_path is not None:
        try:
            registry = load_registry(data_config_path)
        except AssetRegistryError:
            registry = {}
        found = find_asset(registry, kind=kind, canonical_id=canonical_id)
        if found is not None:
            path = ((found[1].get("local") or {}).get("path"))
            if path:
                return Path(str(path)).expanduser()
    return asset_cache_dir(cache_root, kind, canonical_id)


def update_asset_record(
    *,
    kind: AssetKind,
    canonical_id: str,
    data_config_path: str | Path,
    status: str,
    local_path: str | Path | None = None,
    remote_server: str | None = None,
    remote_host: str | None = None,
    remote_path: str | Path | None = None,
    source: str | None = None,
    now: datetime | None = None,
) -> None:
    """Create or update one asset record in `config/data.yaml`."""
    path = Path(data_config_path).expanduser()
    try:
        registry = load_registry(path)
    except AssetRegistryError:
        registry = _new_registry()
    registry = deepcopy(registry)
    bucket = _asset_bucket(registry, kind, create=True)
    found = find_asset(registry, kind=kind, canonical_id=canonical_id)
    key = found[0] if found is not None else _asset_key(canonical_id)
    entry = bucket.setdefault(key, {})
    if not isinstance(entry, dict):
        raise AssetRegistryError(f"资产登记项不是 dict: {kind}:{key}")

    entry.setdefault("kind", kind)
    entry.setdefault("canonical_id", canonical_id)
    entry.setdefault("display_name", canonical_id.rsplit("/", 1)[-1])
    if status:
        entry["status"] = status
    if source:
        entry["last_source"] = source
    if local_path is not None:
        entry.setdefault("local", {})
        entry["local"]["path"] = str(Path(local_path).expanduser())
    if remote_path is not None or remote_server is not None or remote_host is not None:
        entry.setdefault("remote", {})
        if remote_server is not None:
            entry["remote"]["server"] = remote_server
        if remote_host is not None:
            entry["remote"]["host"] = remote_host
        if remote_path is not None:
            entry["remote"]["path"] = str(remote_path)
        remote_location = _remote_location(entry["remote"])
        if remote_location is not None:
            remote_key = (
                remote_location.get("server")
                or remote_location.get("host")
                or remote_location["path"]
            )
            remotes = entry.setdefault("remotes", {})
            if isinstance(remotes, dict):
                remotes[remote_key] = remote_location
    entry["updated_at"] = (now or datetime.now(timezone.utc)).isoformat()
    write_registry(registry, path)


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        raise AssetRegistryError(f"无法读取资产登记簿 {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise AssetRegistryError(f"资产登记簿 YAML 解析失败 {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise AssetRegistryError(f"资产登记簿必须是 dict: {path}")
    return raw


def _asset_bucket(
    registry: dict[str, Any],
    kind: AssetKind,
    *,
    create: bool,
) -> dict[str, Any]:
    assets = registry.setdefault("assets", {}) if create else registry.get("assets", {})
    if not isinstance(assets, dict):
        raise AssetRegistryError("资产登记簿字段 assets 必须是 dict")
    bucket_name = _KIND_BUCKETS[kind]
    bucket = assets.setdefault(bucket_name, {}) if create else assets.get(bucket_name, {})
    if not isinstance(bucket, dict):
        raise AssetRegistryError(f"资产登记簿字段 assets.{bucket_name} 必须是 dict")
    return bucket


def _new_registry() -> dict[str, Any]:
    return {
        "version": 1,
        "defaults": {},
        "assets": {"models": {}, "datasets": {}},
    }


def _asset_dir_name(canonical_id: str) -> str:
    return canonical_id.replace("/", "__")


def _asset_key(canonical_id: str) -> str:
    name = canonical_id.rsplit("/", 1)[-1].lower()
    return name.replace(".", "-").replace("_", "-")


def _remote_location(
    value: dict[str, Any],
    *,
    fallback_server: str | None = None,
) -> dict[str, str] | None:
    path = str(value.get("path") or "").strip()
    if not path:
        return None
    location = {"path": path}
    server = str(value.get("server") or fallback_server or "").strip()
    host = str(value.get("host") or "").strip()
    if server:
        location["server"] = server
    if host:
        location["host"] = host
    return location
