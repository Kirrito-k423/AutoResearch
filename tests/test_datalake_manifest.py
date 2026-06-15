"""Tests for datalake.manifest (Phase 08-04)."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from datalake.manifest import RunManifest, write


def test_run_manifest_serializes_paths_and_datetimes(tmp_path):
    started = datetime(2026, 6, 15, 8, 0, tzinfo=timezone.utc)
    manifest = RunManifest(
        run_id="run123",
        started_at=started,
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/home/t00906153",
        workdir_local=tmp_path / "runs" / "run123",
        one_step={"sum": 5.29, "npu_count": 8, "elapsed_ms": 12, "lib": "verl"},
        exit_code=0,
        wandb_run_id="abc123",
        wandb_path=tmp_path / "runs" / "run123" / "wandb",
        log_files=[tmp_path / "runs" / "run123" / "log.txt"],
        prom_pushed=True,
    )

    payload = manifest.model_dump(mode="json")

    assert payload["started_at"] == "2026-06-15T08:00:00Z"
    assert payload["workdir_local"].endswith("/run123")
    assert payload["log_files"][0].endswith("/log.txt")


def test_write_manifest_creates_run_manifest_json(tmp_path):
    manifest = RunManifest(
        run_id="run123",
        started_at=datetime(2026, 6, 15, 8, 0, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="",
        lib="verl",
        workdir_remote="/root",
        workdir_local=tmp_path / "run123",
    )

    path = write(manifest, root=tmp_path)

    assert path == tmp_path / "run123" / "manifest.json"
    data = json.loads(path.read_text())
    assert data["run_id"] == "run123"
    assert data["server"] == "A2-AK-225"
