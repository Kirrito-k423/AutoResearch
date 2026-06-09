"""Serializable network probe result contracts."""
from __future__ import annotations

from typing import Any, Literal, TypedDict


AttemptMode = Literal["direct", "proxy"]
RowLocation = Literal["local", "remote"]
RowStatus = Literal["ok", "warn", "fail"]


class CurlAttempt(TypedDict):
    """One curl execution attempt for one target."""

    mode: AttemptMode
    target_url: str
    proxy_url: str | None
    exit_code: int
    ok: bool
    status: RowStatus
    http_code: int | None
    latency_ms: int | None
    speed_download_bps: int | None
    error: str | None


class NetworkRow(TypedDict):
    """One target row in the local/remote network matrix."""

    location: RowLocation
    server: str | None
    target_label: str
    target_url: str
    effective_mode: AttemptMode | None
    status: RowStatus
    http_code: int | None
    latency_ms: int | None
    speed_download_bps: int | None
    attempts: list[CurlAttempt]
    error: str | None


class NetworkGroupSummary(TypedDict):
    """Aggregated counts for one location or server."""

    total: int
    passed: int
    warned: int
    failed: int
    needs_proxy: bool
    failed_targets: list[str]


class NetworkSummary(TypedDict):
    """Grouped network matrix summary."""

    total: int
    passed: int
    warned: int
    failed: int
    needs_proxy: bool
    failed_targets: list[str]
    local: NetworkGroupSummary
    remotes: dict[str, NetworkGroupSummary]
    groups: dict[str, NetworkGroupSummary]


class NetworkData(TypedDict):
    """Payload carried in the CheckResult for ``net probe``."""

    rows: list[NetworkRow]
    summary: NetworkSummary
    warnings: list[str]
    metadata: dict[str, Any]
