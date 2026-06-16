"""Pydantic schema for persisted AutoResearch run manifests."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class RunManifest(BaseModel):
    """Local record tying one minimal experiment to collected artifacts."""

    run_id: str = Field(min_length=1)
    started_at: datetime
    finished_at: datetime | None = None
    server: str
    conda_env: str = ""
    lib: str
    workdir_remote: str
    workdir_local: Path
    one_step: dict[str, Any] | None = None
    formal_case: dict[str, Any] | None = None
    exit_code: int | None = None
    error: str | None = None
    config_snapshot: Path | None = None
    provenance: list[dict[str, Any]] = Field(default_factory=list)
    wandb_run_id: str | None = None
    wandb_path: Path | None = None
    log_files: list[Path] = Field(default_factory=list)
    prom_pushed: bool = False
    prom_metrics_file: Path | None = None
