"""YAML → resolve secrets → Pydantic 校验 → Config (D-12, D-13)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from .schema import Config
from ..secrets import resolve_dict, SecretError


DEFAULT_PATH = Path("./config/config.yaml")


class ConfigError(Exception):
    """配置加载/校验失败. message 已是中文格式."""


def _format_validation_error(e: ValidationError, path: str) -> str:
    """把 pydantic ValidationError 翻成中文: 字段路径 + 原因 + 期望."""
    lines = [f"配置错误: {path}"]
    for err in e.errors():
        loc = ".".join(str(x) for x in err["loc"])
        msg = err["msg"]
        typ = err["type"]
        if typ == "missing":
            lines.append(f"  字段 {loc}: 必填但未提供")
        elif typ == "string_too_short":
            min_len = err.get("ctx", {}).get("min_length", "?")
            lines.append(f"  字段 {loc}: 字符串过短 (期望 ≥ {min_len})")
        elif typ == "value_error":
            lines.append(f"  字段 {loc}: {msg}")
        elif typ in ("int_parsing", "int_type"):
            lines.append(f"  字段 {loc}: 期望整数, 收到 {err.get('input', '?')}")
        elif typ == "literal_error":
            expected = err.get("ctx", {}).get("expected", "?")
            lines.append(f"  字段 {loc}: 取值不在允许范围 ({expected})")
        elif typ.startswith("greater_than") or typ.startswith("less_than"):
            lines.append(f"  字段 {loc}: {msg}")
        else:
            lines.append(f"  字段 {loc}: {msg} (type={typ})")
    return "\n".join(lines)


def from_yaml(yaml_text: str) -> Config:
    """从 yaml 文本加载 + 解密 + 校验. 失败抛 ConfigError (中文消息)."""
    try:
        raw: Any = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"配置 YAML 解析失败: {e}") from e

    if not isinstance(raw, dict):
        raise ConfigError(f"配置必须是 dict, 收到 {type(raw).__name__}")

    # 解析所有 <keyring:xxx> / <env:VAR> 占位符
    try:
        resolved = resolve_dict(raw)
    except SecretError as e:
        raise ConfigError(f"配置中敏感字段无法解析: {e}") from e

    # Pydantic 校验
    try:
        cfg = Config.model_validate(resolved)
    except ValidationError as e:
        raise ConfigError(_format_validation_error(e, "config")) from e

    return cfg


def from_path(path: Path | str | None = None) -> Config:
    """从文件路径加载. 优先级: path 参数 > env AUTORESEARCH_CONFIG > 默认路径."""
    if path is None:
        path = os.environ.get("AUTORESEARCH_CONFIG", str(DEFAULT_PATH))
    path = Path(path).expanduser()

    if not path.exists():
        raise ConfigError(f"配置文件不存在: {path}")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ConfigError(f"无法读取配置文件 {path}: {e}") from e

    return from_yaml(text)
