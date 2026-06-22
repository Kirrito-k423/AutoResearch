"""Tests for Prometheus report helpers."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from datalake.manifest import RunManifest

from autoresearch.report.prometheus import build_prom_query, build_prom_query_url, load_prometheus_view


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def _manifest(prom_file: Path | None = None):
    return RunManifest(
        run_id="run123",
        started_at=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        finished_at=datetime(2026, 6, 15, 12, 1, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/root",
        workdir_local=Path("/tmp/run123"),
        prom_pushed=True,
        prom_metrics_file=prom_file,
    )


def test_build_prom_query_helpers():
    assert build_prom_query("run123") == 'autoresearch_npu_count{run_id="run123"}'
    assert "run123" in build_prom_query_url("run123")


def test_load_prometheus_view_prefers_matrix_data():
    payload = {
        "status": "success",
        "data": {"result": [{"values": [[1, "7"], [2, "8"]]}]},
    }
    with patch("autoresearch.report.prometheus.urlopen", return_value=_Response(payload)):
        view = load_prometheus_view(_manifest())

    assert view.available is True
    assert view.current_value == 8.0
    assert len(view.series) == 2


def test_load_prometheus_view_falls_back_to_warning(tmp_path):
    with patch("autoresearch.report.prometheus.urlopen", side_effect=OSError("down")):
        view = load_prometheus_view(_manifest())

    assert view.available is False
    assert "Prometheus 不可达" in (view.warning or "")


def test_load_prometheus_view_includes_evidence_notes(tmp_path):
    prom_file = tmp_path / "prom" / "formal-case-prometheus.json"
    prom_file.parent.mkdir()
    prom_file.write_text(
        json.dumps(
            {
                "run_id": "run123",
                "npu_count": 8,
                "metrics_pushed": ["autoresearch_npu_count"],
                "missing_resource_metrics": ["autoresearch_npu_hbm_used_mib"],
            }
        ),
        encoding="utf-8",
    )
    payload = {"status": "success", "data": {"result": []}}
    with patch("autoresearch.report.prometheus.urlopen", return_value=_Response(payload)):
        view = load_prometheus_view(_manifest(prom_file), base_dir=tmp_path)

    assert view.evidence_path == prom_file
    assert any("NPU 数量" in note for note in view.notes)
    assert any("尚未采集资源指标" in note for note in view.notes)
