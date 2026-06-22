"""Tests for report bundle loading."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from datalake.manifest import RunManifest, write

from autoresearch.report.loader import load_report_bundle


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def _seed_run(tmp_path: Path, *, run_id: str = "run123", with_log: bool = True, with_wandb: bool = True) -> Path:
    run_root = tmp_path / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    log_path = run_root / "log.txt"
    if with_log:
        log_path.write_text(
            "wandb: Run summary:\nSUM= 5.29\nNPU_COUNT= 8\nWANDB_RUN_ID= abc123\n",
            encoding="utf-8",
        )
    wandb_dir = tmp_path / "abc123" / "wandb"
    if with_wandb:
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        (wandb_dir / "files" / "wandb-summary.json").write_text(
            json.dumps({"sum": 5.29, "npu_count": 8, "lib": "verl", "_step": 0}),
            encoding="utf-8",
        )
    manifest = RunManifest(
        run_id=run_id,
        started_at=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        finished_at=datetime(2026, 6, 15, 12, 1, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/root",
        workdir_local=run_root,
        one_step={"sum": 5.29, "npu_count": 8, "elapsed_ms": 1200, "lib": "verl"},
        exit_code=0,
        wandb_run_id="abc123",
        wandb_path=wandb_dir if with_wandb else None,
        log_files=[log_path] if with_log else [],
        prom_pushed=True,
    )
    return write(manifest, root=tmp_path)


def test_load_report_bundle_happy_path(tmp_path):
    _seed_run(tmp_path)
    matrix_payload = {
        "status": "success",
        "data": {"result": [{"values": [[1718452800, "8"], [1718452860, "8"]]}]},
    }
    with patch("autoresearch.report.prometheus.urlopen", return_value=_Response(matrix_payload)):
        bundle = load_report_bundle("run123", root=tmp_path)

    assert bundle.run_id == "run123"
    assert bundle.server == "A2-AK-225"
    assert bundle.log.available is True
    assert any("SUM=" in line for line in bundle.log.key_lines)
    assert bundle.wandb.available is True
    assert bundle.wandb.summary["sum"] == 5.29
    assert bundle.prometheus.available is True
    assert bundle.prometheus.current_value == 8.0
    assert bundle.warnings == []
    assert [skill.name for skill in bundle.skills_used] == ["07 data-collection", "08 experiment-report"]


def test_load_report_bundle_partial_when_artifacts_missing(tmp_path):
    _seed_run(tmp_path, with_log=False, with_wandb=False)
    with patch("autoresearch.report.prometheus.urlopen", side_effect=OSError("boom")):
        bundle = load_report_bundle("run123", root=tmp_path)

    assert bundle.log.available is False
    assert bundle.wandb.available is False
    assert bundle.prometheus.available is False
    assert len(bundle.warnings) == 3
    assert "缺少本地日志产物" in bundle.warnings[0]
