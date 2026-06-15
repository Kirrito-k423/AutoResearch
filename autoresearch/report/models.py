"""Data models for local experiment reports."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MetricPoint:
    """One point for a tiny inline metric chart."""

    x: float
    y: float
    label: str = ""


@dataclass(frozen=True)
class ArtifactLink:
    """A file or service link surfaced in the report."""

    label: str
    href: str
    note: str = ""


@dataclass
class LogView:
    """Renderable summary of a local run log."""

    available: bool
    path: Path | None
    key_lines: list[str] = field(default_factory=list)
    tail_lines: list[str] = field(default_factory=list)
    warning: str | None = None


@dataclass
class WandbView:
    """Renderable summary of the local wandb artifact for a run."""

    available: bool
    run_id: str | None
    local_path: Path | None
    service_url: str
    summary: dict[str, Any] = field(default_factory=dict)
    charts: dict[str, list[MetricPoint]] = field(default_factory=dict)
    links: list[ArtifactLink] = field(default_factory=list)
    warning: str | None = None


@dataclass
class PrometheusView:
    """Renderable summary of local Prometheus metrics for a run."""

    available: bool
    metric_name: str
    query: str
    query_url: str
    service_url: str
    current_value: float | None = None
    series: list[MetricPoint] = field(default_factory=list)
    warning: str | None = None


@dataclass
class ReportBundle:
    """Normalized, partial-friendly report payload."""

    run_id: str
    manifest_path: Path
    started_at: datetime
    finished_at: datetime | None
    server: str
    conda_env: str
    lib: str
    workdir_remote: str
    workdir_local: Path
    exit_code: int | None
    error: str | None
    one_step: dict[str, Any] | None
    artifact_links: list[ArtifactLink]
    warnings: list[str]
    log: LogView
    wandb: WandbView
    prometheus: PrometheusView
