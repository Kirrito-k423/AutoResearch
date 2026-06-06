"""~/.ssh/config alias + user@host[:port] 解析 (D-01 + CORE-SSH-02)."""
from __future__ import annotations

import getpass
from dataclasses import dataclass
from pathlib import Path

import paramiko

from .exceptions import HostResolveError


@dataclass(frozen=True)
class HostSpec:
    """解析后的目标主机规格."""

    alias: str | None       # 原始 alias (alias 形式有, 直接形式无)
    host: str               # 实际 hostname 或 IP
    port: int               # SSH 端口 (默认 22)
    user: str               # 用户名
    identity_file: Path | None  # IdentityFile 路径 (可能 None)


def resolve_host(target: str) -> HostSpec:
    """解析目标字符串为 HostSpec.

    包含 '@' → 解析为 user@host[:port] 直接形式.
    否则 → 当作 alias, 查 ~/.ssh/config.
    """
    if "@" in target:
        return _parse_direct(target)
    return _parse_ssh_config(target)


def _parse_direct(target: str) -> HostSpec:
    """解析 user@host[:port] 形式."""
    try:
        user, rest = target.split("@", 1)
    except ValueError as e:
        raise HostResolveError(f"无法解析目标 '{target}': 缺少 '@' 分隔符") from e
    if not user or not rest:
        raise HostResolveError(f"无法解析目标 '{target}': user/host 不能为空")

    if ":" in rest:
        host, port_s = rest.rsplit(":", 1)
        try:
            port = int(port_s)
        except ValueError as e:
            raise HostResolveError(
                f"无法解析目标 '{target}': port '{port_s}' 不是整数"
            ) from e
        if not (1 <= port <= 65535):
            raise HostResolveError(f"无法解析目标 '{target}': port {port} 越界")
        return HostSpec(alias=None, host=host, port=port, user=user, identity_file=None)

    return HostSpec(alias=None, host=rest, port=22, user=user, identity_file=None)


def _parse_ssh_config(alias: str) -> HostSpec:
    """从 ~/.ssh/config 解析 alias."""
    config_path = Path.home() / ".ssh" / "config"
    if not config_path.exists():
        raise HostResolveError(
            f"未找到 ssh config: {config_path}; alias='{alias}' 仅支持直接 user@host 形式"
        )

    try:
        ssh_config = paramiko.SSHConfig.from_file(str(config_path))
    except Exception as e:
        raise HostResolveError(f"解析 ssh config {config_path} 失败: {e}") from e

    conf = ssh_config.lookup(alias)
    if not conf or "hostname" not in conf:
        raise HostResolveError(
            f"ssh config 中找不到 alias='{alias}' (config={config_path}); "
            f"可用 alias: {list(ssh_config.get_hostnames())}"
        )

    host = conf["hostname"]
    try:
        port = int(conf.get("port", 22))
    except (TypeError, ValueError) as e:
        raise HostResolveError(f"alias='{alias}' port 字段非法: {e}") from e

    user = conf.get("user") or _current_user()
    id_file: Path | None = None
    if "identityfile" in conf:
        ids = conf["identityfile"]
        # paramiko 可能返回 list 或 str
        if isinstance(ids, list):
            if ids:
                id_file = Path(ids[0])
        else:
            id_file = Path(ids)

    return HostSpec(
        alias=alias, host=host, port=port, user=user, identity_file=id_file
    )


def _current_user() -> str:
    try:
        return getpass.getuser()
    except Exception:
        return "root"
