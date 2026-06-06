"""__AR_PROGRESS__=<json> 协议 (D-14, D-15).

D-04e 锁定: 最终 stdout 唯一 JSON 对象.
D-04d 锁定: 进度走 stderr, 格式 __AR_PROGRESS__=<json>.
"""
from __future__ import annotations

import datetime
import json
import sys
from typing import Any, Literal


PROGRESS_PREFIX: str = "__AR_PROGRESS__="
"""stderr 行前缀. 下游消费者 (Archon / 自家 pipeline) grep 这个标记."""

Level = Literal["info", "warn", "error"]


def emit_progress(
    stage: str,
    *,
    level: Level = "info",
    data: dict[str, Any] | None = None,
    **fields: Any,
) -> None:
    """发一条进度事件到 stderr.

    Args:
        stage: 阶段名 (e.g. 'ssh.connect', 'secrets.resolve', 'config.load')
        level: info/warn/error
        data: 可选 dict, 写入 JSON.data 字段
        **fields: 任意附加字段, 展开到 JSON 顶层

    Output: stderr 一行, 格式 '__AR_PROGRESS__=<json>'
    """
    payload: dict[str, Any] = {
        "stage": stage,
        "ts": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(timespec="seconds"),
        "level": level,
    }
    if data is not None:
        payload["data"] = data
    payload.update(fields)

    line = PROGRESS_PREFIX + json.dumps(payload, ensure_ascii=False)
    print(line, file=sys.stderr, flush=True)


# TypedDict-friendly 容器 (用于类型注解 / 单元测试 mock)
class ProgressEvent(dict):
    """一帧进度事件 (dict subclass, 无强制 schema)."""

    def __init__(
        self,
        stage: str,
        level: Level = "info",
        data: dict | None = None,
        **fields: Any,
    ) -> None:
        super().__init__(
            stage=stage,
            ts=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(timespec="seconds"),
            level=level,
            data=data or {},
            **fields,
        )
