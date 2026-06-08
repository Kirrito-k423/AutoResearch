"""autoresearch config keyring — 写读 macOS Keychain / 系统 keyring.

设计:
- 复用 workspace_core.secrets.KEYRING_AVAILABLE 探测 (Phase 2 沉淀)
- 4 action: set / get / delete / list
- keyring 不可用时返中文错误
- service name 固定 'autoresearch'
"""
from __future__ import annotations

import sys
from typing import Any

from workspace_core.secrets import KEYRING_AVAILABLE


SERVICE = "autoresearch"


def _backend_or_die(lang: str):
    """返 keyring module 或 None (不可用时打印中文错误)."""
    if not KEYRING_AVAILABLE:
        msg = (
            "错误: keyring 不可用. 装 'keyring' 包 (uv add keyring) 或 macOS 上启用 Keychain."
            if lang == "zh"
            else "Error: keyring unavailable. Install 'keyring' package or enable macOS Keychain."
        )
        print(msg, file=sys.stderr)
        return None
    import keyring
    return keyring


def run_keyring(
    *, action: str, name: str, value: str | None = None, lang: str = "zh"
) -> int:
    """Keyring 子命令主入口.

    Args:
        action: 'set' | 'get' | 'delete' | 'list'
        name: 名字 (用作 keyring username)
        value: set 时必传

    Returns:
        exit code: 0 = ok, 1 = 错, 2 = 不可用
    """
    keyring = _backend_or_die(lang)
    if keyring is None:
        return 2

    try:
        if action == "set":
            if value is None:
                msg = (
                    "错误: keyring set 需 --value"
                    if lang == "zh"
                    else "Error: keyring set requires --value"
                )
                print(msg, file=sys.stderr)
                return 1
            keyring.set_password(SERVICE, name, value)
            print(
                f"✅ 已存到 keyring: {SERVICE}/{name}"
                if lang == "zh"
                else f"✅ Saved: {SERVICE}/{name}"
            )
            return 0

        if action == "get":
            v = keyring.get_password(SERVICE, name)
            if v is None:
                print("(无)" if lang == "zh" else "(none)")
                return 1
            print(v)
            return 0

        if action == "delete":
            try:
                keyring.delete_password(SERVICE, name)
                print(
                    f"✅ 已删: {SERVICE}/{name}"
                    if lang == "zh"
                    else f"✅ Deleted: {SERVICE}/{name}"
                )
                return 0
            except keyring.errors.PasswordDeleteError:
                msg = (
                    f"未找到: {SERVICE}/{name}"
                    if lang == "zh"
                    else f"Not found: {SERVICE}/{name}"
                )
                print(msg, file=sys.stderr)
                return 1

        if action == "list":
            print(
                "(keyring 没原生 list API; 用 'get <name>' 探测存在)"
                if lang == "zh"
                else "(keyring has no list API; probe with 'get <name>')"
            )
            return 0

        msg = (
            f"未知 action: {action} (应 set/get/delete/list)"
            if lang == "zh"
            else f"Unknown action: {action}"
        )
        print(msg, file=sys.stderr)
        return 1
    except Exception as e:
        msg = f"keyring 错误: {e}" if lang == "zh" else f"keyring error: {e}"
        print(msg, file=sys.stderr)
        return 1
