"""autoresearch config show — 脱敏打印配置 (CFG-SHOW-01).

设计 (D-05):
- 字段名匹配 (?i)(password|secret|token|credential) → 值 '***'
- 例外: identity_file, keyring
- 嵌套 dict / list 递归
- 保留字段名, 让用户能定位
- --json 返 JSON (脱敏后)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from workspace_core.config import from_path, ConfigError
from ._common import resolve_config_path


# 敏感字段名正则 (case-insensitive)
_SENSITIVE_RE = re.compile(r"(?i)(password|secret|token|credential)")
# 例外 (不是敏感): 路径/名字/占位符
_SAFE_FIELDS = {"identity_file", "keyring"}


def _is_sensitive(key: str) -> bool:
    """字段名是否敏感.

    True 触发该字段值脱敏.
    """
    if key.lower() in _SAFE_FIELDS:
        return False
    return bool(_SENSITIVE_RE.search(key))


def _redact(value: Any, *, in_sensitive: bool = False) -> Any:
    """递归脱敏. in_sensitive=True 时字符串值 → '***'."""
    if in_sensitive and isinstance(value, str):
        return "***"
    if isinstance(value, dict):
        return {k: _redact(v, in_sensitive=_is_sensitive(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact(item, in_sensitive=in_sensitive) for item in value]
    return value


def _to_yaml_like(data: Any, indent: int = 0) -> str:
    """简易 YAML 风格打印 (够用即可)."""
    sp = "  " * indent
    if isinstance(data, dict):
        lines = []
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.append(_to_yaml_like(v, indent + 1))
            else:
                lines.append(f"{sp}{k}: {v!r}")
        return "\n".join(lines)
    if isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{sp}-")
                lines.append(_to_yaml_like(item, indent + 1))
            else:
                lines.append(f"{sp}- {item!r}")
        return "\n".join(lines)
    return f"{sp}{data!r}"


def run_show(
    *, config: str | None = None, lang: str = "zh", as_json: bool = False
) -> int:
    """Show 子命令主入口.

    Returns:
        exit code: 0 = ok, 1 = 读/解析失败
    """
    target = resolve_config_path(config)
    try:
        cfg = from_path(target)
    except ConfigError as e:
        if as_json:
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        else:
            msg = (
                f"❌ 读 config 失败: {target}"
                if lang == "zh"
                else f"❌ Read failed: {target}"
            )
            print(msg, file=sys.stderr)
            print(str(e), file=sys.stderr)
        return 1

    # Pydantic v2 model_dump
    raw = cfg.model_dump()
    redacted = _redact(raw)

    if as_json:
        print(json.dumps(redacted, ensure_ascii=False, indent=2))
    else:
        if lang == "zh":
            print(f"# {target} (敏感字段已脱敏):")
        else:
            print(f"# {target} (sensitive fields redacted):")
        print(_to_yaml_like(redacted))
    return 0
