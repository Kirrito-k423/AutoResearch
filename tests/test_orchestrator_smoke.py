"""Tests for `autoresearch run smoke` orchestration."""
from __future__ import annotations

import json
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.orchestrator.smoke import run_smoke


def test_run_smoke_collect_then_report_success():
    collect_payload = {"ok": True, "run_id": "run123", "manifest": "/tmp/manifest.json"}
    report_payload = {"ok": True, "run_id": "run123", "report": "/tmp/report.html"}

    with patch("autoresearch.orchestrator.smoke.run_collect", return_value=(0, collect_payload)) as collect, \
         patch("autoresearch.orchestrator.smoke.run_render", return_value=(0, report_payload)) as render:
        exit_code, payload = run_smoke(
            server="A2-AK-225",
            lib="verl",
            config="config/config.yaml",
            timeout=60.0,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["failed_step"] is None
    assert payload["run_id"] == "run123"
    assert payload["manifest"] == "/tmp/manifest.json"
    assert payload["report"] == "/tmp/report.html"
    assert collect.call_args.kwargs["server"] == "A2-AK-225"
    assert render.call_args.kwargs["run_id"] == "run123"


def test_run_smoke_waits_for_prometheus_when_metrics_were_pushed():
    collect_payload = {
        "ok": True,
        "run_id": "run123",
        "manifest": "/tmp/manifest.json",
        "prom_pushed": True,
    }
    report_payload = {"ok": True, "run_id": "run123", "report": "/tmp/report.html"}

    with patch("autoresearch.orchestrator.smoke.run_collect", return_value=(0, collect_payload)), \
         patch("autoresearch.orchestrator.smoke._wait_for_prometheus_metric", return_value=True) as wait, \
         patch("autoresearch.orchestrator.smoke.run_render", return_value=(0, report_payload)) as render:
        exit_code, payload = run_smoke(
            server="A2-AK-225",
            prometheus_url="http://localhost:9090",
            prometheus_wait=5.0,
        )

    assert exit_code == 0
    assert payload["prometheus_ready"] is True
    assert wait.call_args.args == ("run123",)
    assert wait.call_args.kwargs["timeout"] == 5.0
    assert render.call_args.kwargs["run_id"] == "run123"


def test_run_smoke_collect_failure_skips_report():
    collect_payload = {
        "ok": False,
        "run_id": "run123",
        "errors": ["minimal failed: boom"],
    }

    with patch("autoresearch.orchestrator.smoke.run_collect", return_value=(1, collect_payload)), \
         patch("autoresearch.orchestrator.smoke.run_render") as render:
        exit_code, payload = run_smoke(server="A2-AK-225")

    assert exit_code == 1
    assert payload["failed_step"] == "collect"
    assert payload["steps"][0]["diagnosis"] == "minimal failed: boom"
    assert payload["steps"][1]["status"] == "skipped"
    render.assert_not_called()


def test_run_smoke_report_failure_points_to_report():
    collect_payload = {"ok": True, "run_id": "run123", "manifest": "/tmp/manifest.json"}
    report_payload = {"ok": False, "run_id": "run123", "error": "missing manifest"}

    with patch("autoresearch.orchestrator.smoke.run_collect", return_value=(0, collect_payload)), \
         patch("autoresearch.orchestrator.smoke.run_render", return_value=(1, report_payload)):
        exit_code, payload = run_smoke(server="A2-AK-225")

    assert exit_code == 1
    assert payload["failed_step"] == "report"
    assert payload["steps"][1]["diagnosis"] == "missing manifest"


def test_run_smoke_missing_run_id_fails_report_step():
    with patch("autoresearch.orchestrator.smoke.run_collect", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.smoke.run_render") as render:
        exit_code, payload = run_smoke(server="A2-AK-225")

    assert exit_code == 1
    assert payload["failed_step"] == "report"
    assert payload["steps"][1]["diagnosis"] == "collect step succeeded but did not return run_id"
    render.assert_not_called()


def test_run_smoke_cli_outputs_single_json_object():
    runner = CliRunner()
    payload = {"ok": True, "command": "smoke", "run_id": "run123"}

    with patch("autoresearch.orchestrator.smoke.run_smoke", return_value=(0, payload)) as mock:
        result = runner.invoke(
            main,
            [
                "run",
                "smoke",
                "--server",
                "A2-AK-225",
                "--lib",
                "verl",
                "--timeout",
                "12",
                "--pushgateway-url",
                "http://127.0.0.1:17891",
            ],
        )

    assert result.exit_code == 0
    assert json.loads(result.output) == payload
    assert mock.call_args.kwargs["server"] == "A2-AK-225"
    assert mock.call_args.kwargs["timeout"] == 12.0
