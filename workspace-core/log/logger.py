"""统一日志接口 (D-16, CORE-LOG-01).

get_logger(name) → logger; configure_root 配 stderr (人类可读) + 文件 (JSON) handler.
8 skill 不直接配 handler, 全部走这个入口.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from .formatter import HumanFormatter, JsonFormatter


_LOGGERS: dict[str, logging.Logger] = {}
_DEFAULT_LEVEL = logging.INFO


def configure_root(
    level: int = _DEFAULT_LEVEL,
    log_file: Path | None = None,
    enable_stderr: bool = True,
) -> None:
    """配置 root logger.

    Args:
        level: 日志级别 (logging.INFO 等)
        log_file: 可选, 落 JSON 行到这个文件 (parent dirs 自动建)
        enable_stderr: 是否输出到 stderr (人类可读)
    """
    root = logging.getLogger()
    root.setLevel(level)
    # 清掉旧 handler (idempotent, 重复配不会堆 handler)
    for h in list(root.handlers):
        root.removeHandler(h)

    if enable_stderr:
        h = logging.StreamHandler(sys.stderr)
        h.setFormatter(HumanFormatter())
        root.addHandler(h)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(JsonFormatter())
        root.addHandler(fh)


def get_logger(name: str) -> logging.Logger:
    """取 logger. 缓存同名, 不自动加 handler (由 configure_root 管)."""
    if name not in _LOGGERS:
        _LOGGERS[name] = logging.getLogger(name)
    return _LOGGERS[name]
