"""Tests for autoresearch.collect.manifest (Phase 08-04)."""
from __future__ import annotations

from datetime import datetime, timezone

from workspace_core.config import ServerSpec

from autoresearch.collect.manifest import build_manifest


def test_build_manifest_maps_minimal_result_to_run_manifest(tmp_path):
    spec = ServerSpec(
        name="A2-AK-225",
        host="192.168.9.225",
        user="root",
        workdir="/home/t00906153",
    )
    started = datetime(2026, 6, 15, 8, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 6, 15, 8, 1, tzinfo=timezone.utc)

    manifest = build_manifest(
        "run123",
        spec,
        "verl",
        "verl-qwen3.5",
        "/home/t00906153",
        {
            "lib": "verl",
            "sum_value": 5.29,
            "npu_count": 8,
            "elapsed_ms": 1234,
            "exit_code": 0,
            "wandb_run_id": "abc123",
        },
        tmp_path / "run123" / "wandb",
        tmp_path / "run123" / "log.txt",
        True,
        started_at=started,
        finished_at=finished,
        local_runs_root=tmp_path,
    )

    assert manifest.run_id == "run123"
    assert manifest.server == "A2-AK-225"
    assert manifest.workdir_local == tmp_path / "run123"
    assert manifest.one_step == {
        "sum": 5.29,
        "npu_count": 8,
        "elapsed_ms": 1234,
        "lib": "verl",
    }
    assert manifest.wandb_run_id == "abc123"
    assert manifest.prom_pushed is True


def test_build_manifest_combines_errors(tmp_path):
    spec = ServerSpec(name="A2-AK-225", host="192.168.9.225", user="root")

    manifest = build_manifest(
        "run123",
        spec,
        "verl",
        "",
        "/root",
        {"lib": "verl", "exit_code": 1, "error": "remote failed"},
        None,
        None,
        False,
        error="log missing",
        local_runs_root=tmp_path,
    )

    assert manifest.error == "remote failed; log missing"
    assert manifest.log_files == []
    assert manifest.prom_pushed is False
