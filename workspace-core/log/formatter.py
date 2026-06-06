"""日志 Formatter: 人类可读 (CLI) + JSON (文件)."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone


_ANSI = {
    "DEBUG": "\033[90m",      # 灰
    "INFO": "\033[36m",       # 青
    "WARNING": "\033[33m",    # 黄
    "ERROR": "\033[31m",      # 红
    "CRITICAL": "\033[1;31m", # 粗红
    "RESET": "\033[0m",
}


class HumanFormatter(logging.Formatter):
    """人类可读 + ANSI 颜色 (stderr TTY 才显示, 重定向到 file 时无效)."""

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime("%H:%M:%S")
        level = record.levelname
        color = _ANSI.get(level, "")
        reset = _ANSI["RESET"]
        name = record.name
        msg = record.getMessage()
        ctx = getattr(record, "ctx", None)
        ctx_str = f" ctx={ctx}" if ctx else ""
        return f"{ts} {color}{level:<7}{reset} {name}: {msg}{ctx_str}"


class JsonFormatter(logging.Formatter):
    """JSON 行格式 (落文件, 供 datalake 后续 ingest)."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if hasattr(record, "host") and record.host:
            payload["host"] = record.host
        if hasattr(record, "ctx") and record.ctx:
            payload["ctx"] = record.ctx
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)
