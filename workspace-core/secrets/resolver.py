"""敏感字段占位符解析 (D-06..09)."""
from __future__ import annotations

import os
import re
import sys
import warnings
from typing import Final


PLACEHOLDER_RE: Final = re.compile(r"^<(keyring|env):([A-Za-z0-9_\-]+)>$")


class SecretError(Exception):
    """无法解析占位符. 包含占位符字符串 + 尝试过的 backend."""


try:
    import keyring
    KEYRING_AVAILABLE: bool = True
    _KEYRING_IMPORT_ERROR: str | None = None
except ImportError as e:
    KEYRING_AVAILABLE = False
    _KEYRING_IMPORT_ERROR = str(e)
    keyring = None  # type: ignore


_warned_keyring_failure: bool = False


def _warn_keyring_failure_once() -> None:
    """软失败警告只发一次 (避免重复 noise)."""
    global _warned_keyring_failure
    if not _warned_keyring_failure:
        msg = (
            "⚠ workspace-core.secrets: keyring 不可用 ("
            + (_KEYRING_IMPORT_ERROR or "unknown")
            + "); <keyring:xxx> 将 fallback 到 <env:xxx> 解析. "
            "首次启动可忽略, 生产环境请装 keyring 包."
        )
        warnings.warn(msg, stacklevel=2)
        print(msg, file=sys.stderr)
        _warned_keyring_failure = True


def _try_keyring(name: str) -> str | None:
    if not KEYRING_AVAILABLE or keyring is None:
        return None
    try:
        return keyring.get_password("autoresearch", name)
    except Exception:
        _warn_keyring_failure_once()
        return None


def _try_env(var: str) -> str | None:
    return os.environ.get(var)


def resolve_secret(value: str) -> str:
    """解析占位符, 返回真实值.

    - '<keyring:NAME>' → keyring.get_password('autoresearch', NAME) 失败时 fallback env
    - '<env:VAR>'      → os.environ['VAR']
    - 其他              → 原样返回

    Raises:
        SecretError: 已知占位符但所有 backend 都没找到
    """
    if not isinstance(value, str):
        return value

    m = PLACEHOLDER_RE.match(value)
    if not m:
        return value  # 非占位符, 原样

    kind, name = m.group(1), m.group(2)

    if kind == "keyring":
        v = _try_keyring(name)
        if v is not None:
            return v
        # D-09 软失败: fallback env
        v = _try_env(name)
        if v is not None:
            _warn_keyring_failure_once()
            return v
        raise SecretError(
            f"无法解析占位符 {value}; keyring 不可用 + env {name} 未设置"
        )

    if kind == "env":
        v = _try_env(name)
        if v is not None:
            return v
        raise SecretError(f"无法解析占位符 {value}; env {name} 未设置")

    raise SecretError(f"未知占位符类型: {kind}")


def resolve_dict(d: dict) -> dict:
    """递归解析 dict 中所有 value 为占位符的项 (含 list of dict / list of str)."""
    out: dict = {}
    for k, v in d.items():
        if isinstance(v, str):
            out[k] = resolve_secret(v)
        elif isinstance(v, dict):
            out[k] = resolve_dict(v)
        elif isinstance(v, list):
            out[k] = [
                resolve_dict(i) if isinstance(i, dict)
                else (resolve_secret(i) if isinstance(i, str) else i)
                for i in v
            ]
        else:
            out[k] = v
    return out
