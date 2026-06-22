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


@dataclass(frozen=True)
class SkillUsage:
    """A repository skill involved in producing or reading this run."""

    name: str
    path: str
    purpose: str


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
    run_links: list[ArtifactLink] = field(default_factory=list)
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
    resource_series: dict[str, list[MetricPoint]] = field(default_factory=dict)
    sample_interval_seconds: int | None = None
    evidence_path: Path | None = None
    notes: list[str] = field(default_factory=list)
    warning: str | None = None


@dataclass(frozen=True)
class ArtifactStatus:
    """Local formal-case artifact availability."""

    name: str
    path: Path | None
    ok: bool
    warning: str | None = None
    key: str | None = None


@dataclass(frozen=True)
class VerlCaseMatrixRowView:
    """One formal Verl case matrix row for reports."""

    input_tokens: int
    output_tokens: int
    mode: str
    status: str
    tokens_per_second: float | None
    latency_ms: float | None
    sample_count: int
    accuracy: float | None
    consistency: float | None
    error: str | None = None


@dataclass
class VerlCaseView:
    """Normalized formal Verl case report data."""

    available: bool
    complete_matrix: bool
    rows: list[VerlCaseMatrixRowView] = field(default_factory=list)
    length_summary: list[dict[str, Any]] = field(default_factory=list)
    mode_summary: list[dict[str, Any]] = field(default_factory=list)
    async_comparison: list[dict[str, Any]] = field(default_factory=list)
    accuracy_overall: float | None = None
    consistency_overall: float | None = None
    trainer_val_only: bool | None = None
    training_mode: str = ""
    score_diagnostics: list[str] = field(default_factory=list)
    artifacts: list[ArtifactStatus] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


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
    formal_case: VerlCaseView | None = None
    skills_used: list[SkillUsage] = field(default_factory=list)
