"""workspace-core.secrets — 敏感字段占位符解析 (D-06..09).

支持的占位符:
- <keyring:NAME>  从系统 keyring 取
- <env:VAR>       从 env 取

keyring 不可用时 (D-09 软失败): warning + fallback env lookup.
"""
from .resolver import (
    resolve_secret,
    resolve_dict,
    SecretError,
    KEYRING_AVAILABLE,
    PLACEHOLDER_RE,
)

__all__ = [
    "resolve_secret",
    "resolve_dict",
    "SecretError",
    "KEYRING_AVAILABLE",
    "PLACEHOLDER_RE",
]
