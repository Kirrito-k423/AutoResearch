"""autoresearch.reach.models — TypedDict definitions for reach results."""
from __future__ import annotations

from typing import TypedDict


class ReachCheck(TypedDict):
    """Single endpoint reach check (wandb or pushgateway)."""

    name: str                  # "wandb" / "pushgateway"
    ok: bool
    latency_ms: int | None
    status_code: int | None
    detail: str | None         # 错误信息 or extra context
    warning: str | None        # best-effort warn (D-38.D4 push 失败)


class ReachResult(TypedDict):
    """Per-server reach test result."""

    server: str                # config alias
    ok: bool
    severity: str              # "ok" / "warn" / "fail"
    wandb: ReachCheck
    pushgateway: ReachCheck
    host: str                  # actual SSH host (sanitized)
    tunnel_wandb: str | None   # 17890 tunnel state 摘要
    tunnel_pushgateway: str | None  # 17891 tunnel info
    error: str | None          # 整体失败原因 (含 D-37.C2 文案)


class ReachSummary(TypedDict):
    """Aggregate reach result (--all 用)."""

    total: int
    passed: int
    failed: int
    warned: int
    passed_servers: list[str]
    failed_servers: list[str]
    results: dict[str, ReachResult]
