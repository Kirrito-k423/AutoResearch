"""Tests for local wandb report helpers."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from datalake.manifest import RunManifest

from autoresearch.report.wandb import load_wandb_view


def test_load_wandb_view_reads_summary_and_builds_links(tmp_path):
    wandb_dir = tmp_path / "wandb"
    (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
    (wandb_dir / "files" / "wandb-summary.json").write_text(
        json.dumps({"sum": 3.21, "npu_count": 8, "_step": 0}),
        encoding="utf-8",
    )
    manifest = RunManifest(
        run_id="run123",
        started_at=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/root",
        workdir_local=tmp_path / "run123",
        wandb_run_id="abc123",
        wandb_path=wandb_dir,
    )

    view = load_wandb_view(manifest)

    assert view.available is True
    assert view.run_id == "abc123"
    assert view.summary["sum"] == 3.21
    assert "sum" in view.charts
    assert view.links[0].href == "http://localhost:8080"


def test_load_wandb_view_handles_missing_summary(tmp_path):
    manifest = RunManifest(
        run_id="run123",
        started_at=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/root",
        workdir_local=tmp_path / "run123",
        wandb_run_id="abc123",
        wandb_path=tmp_path / "wandb",
    )

    view = load_wandb_view(manifest)

    assert view.available is False
    assert "缺少 wandb summary" in (view.warning or "")
