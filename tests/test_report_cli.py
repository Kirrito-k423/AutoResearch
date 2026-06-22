"""Tests for report render CLI."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.report.cli import run_render
from autoresearch.report.models import ArtifactLink, LogView, PrometheusView, ReportBundle, WandbView


def _bundle(tmp_path: Path) -> ReportBundle:
    run_root = tmp_path / "run123"
    run_root.mkdir(parents=True, exist_ok=True)
    manifest = run_root / "manifest.json"
    manifest.write_text("{}", encoding="utf-8")
    return ReportBundle(
        run_id="run123",
        manifest_path=manifest,
        started_at=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        finished_at=datetime(2026, 6, 15, 12, 1, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/root",
        workdir_local=run_root,
        exit_code=0,
        error=None,
        one_step={"sum": 5.29, "npu_count": 8, "elapsed_ms": 1200},
        artifact_links=[ArtifactLink(label="manifest.json", href=manifest.as_uri())],
        warnings=[],
        log=LogView(available=True, path=run_root / "log.txt", key_lines=["SUM= 5.29"], tail_lines=["SUM= 5.29"]),
        wandb=WandbView(available=False, run_id="abc123", local_path=None, service_url="http://localhost:8080"),
        prometheus=PrometheusView(
            available=False,
            metric_name="autoresearch_npu_count",
            query='autoresearch_npu_count{run_id="run123"}',
            query_url="http://localhost:9090/graph",
            service_url="http://localhost:9090",
        ),
    )


def test_run_render_can_open_report(tmp_path):
    bundle = _bundle(tmp_path)
    with patch("autoresearch.report.cli.load_report_bundle", return_value=bundle), \
         patch("autoresearch.report.cli.webbrowser.open_new_tab", return_value=True):
        exit_code, payload = run_render(run_id="run123", open_report=True)

    assert exit_code == 0
    assert payload["opened"] is True
    assert Path(payload["report"]).exists()


def test_run_render_accepts_manifest_path(tmp_path):
    bundle = _bundle(tmp_path)
    with patch("autoresearch.report.cli.load_report_bundle_from_manifest", return_value=bundle):
        exit_code, payload = run_render(
            run_id="",
            manifest_path=bundle.manifest_path,
            open_report=False,
        )

    assert exit_code == 0
    assert payload["run_id"] == "run123"
    assert Path(payload["report"]).exists()


def test_report_render_cli_outputs_single_json_object():
    runner = CliRunner()
    with patch(
        "autoresearch.report.cli.run_render",
        return_value=(0, {"ok": True, "run_id": "run123", "report": "/tmp/report.html", "opened": False, "warnings": []}),
    ):
        result = runner.invoke(main, ["report", "render", "--run-id", "run123"])

    assert result.exit_code == 0
    assert json.loads(result.output)["run_id"] == "run123"
