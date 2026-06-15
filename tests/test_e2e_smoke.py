"""Tests for `autoresearch e2e smoke`."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.e2e.report_check import check_report_completeness
from autoresearch.e2e.smoke import run_e2e_smoke


def _bundle(
    tmp_path: Path,
    *,
    report_html: bool = True,
    log: bool = True,
    wandb: bool = True,
    prometheus: bool = True,
):
    run_root = tmp_path / "run123"
    run_root.mkdir(parents=True, exist_ok=True)
    manifest_path = run_root / "manifest.json"
    manifest_path.write_text("{}", encoding="utf-8")
    if report_html:
        (run_root / "report.html").write_text("<html></html>", encoding="utf-8")

    return SimpleNamespace(
        manifest_path=manifest_path,
        warnings=[],
        log=SimpleNamespace(
            available=log,
            path=run_root / "log.txt" if log else None,
            warning=None if log else "缺少本地日志产物",
        ),
        wandb=SimpleNamespace(
            available=wandb,
            local_path=tmp_path / "wandb" if wandb else None,
            warning=None if wandb else "缺少 wandb artifact",
        ),
        prometheus=SimpleNamespace(
            available=prometheus,
            query='autoresearch_npu_count{run_id="run123"}',
            warning=None if prometheus else "Prometheus missing metric",
        ),
    )


def test_check_report_completeness_passes_when_all_views_exist(tmp_path):
    with patch("autoresearch.e2e.report_check.load_report_bundle", return_value=_bundle(tmp_path)):
        exit_code, payload = check_report_completeness(run_id="run123")

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["missing"] == []
    assert payload["checks"]["log"]["ok"] is True
    assert payload["checks"]["wandb"]["ok"] is True
    assert payload["checks"]["prometheus"]["ok"] is True


def test_check_report_completeness_fails_when_view_missing(tmp_path):
    bundle = _bundle(tmp_path, prometheus=False)

    with patch("autoresearch.e2e.report_check.load_report_bundle", return_value=bundle):
        exit_code, payload = check_report_completeness(run_id="run123")

    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["missing"] == ["prometheus"]
    assert payload["checks"]["prometheus"]["warning"] == "Prometheus missing metric"


def test_check_report_completeness_fails_when_html_missing(tmp_path):
    bundle = _bundle(tmp_path, report_html=False)

    with patch("autoresearch.e2e.report_check.load_report_bundle", return_value=bundle):
        exit_code, payload = check_report_completeness(run_id="run123")

    assert exit_code == 1
    assert payload["missing"] == ["html"]


def _patch_e2e_success():
    return (
        patch("autoresearch.e2e.smoke.run_check_all", return_value=(0, {"ok": True})),
        patch(
            "autoresearch.e2e.smoke.run_smoke",
            return_value=(0, {"ok": True, "run_id": "run123", "report": "/tmp/report.html"}),
        ),
        patch(
            "autoresearch.e2e.smoke.check_report_completeness",
            return_value=(0, {"ok": True, "run_id": "run123", "report": "/tmp/report.html"}),
        ),
        patch("autoresearch.e2e.smoke._check_archon_observable", return_value=(0, {"ok": True})),
    )


def test_run_e2e_smoke_happy_path():
    patches = _patch_e2e_success()
    with patches[0], patches[1], patches[2], patches[3]:
        exit_code, payload = run_e2e_smoke(server="A2-AK-225", lib="verl")

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["failed_step"] is None
    assert [step["id"] for step in payload["steps"]] == [
        "readiness",
        "smoke",
        "report",
        "archon",
        "duration",
    ]
    assert payload["run_id"] == "run123"
    assert payload["report"] == "/tmp/report.html"


def test_run_e2e_smoke_readiness_failure_skips_downstream():
    with patch("autoresearch.e2e.smoke.run_check_all", return_value=(1, {"ok": False, "error": "bad config"})), \
         patch("autoresearch.e2e.smoke.run_smoke") as smoke:
        exit_code, payload = run_e2e_smoke(server="A2-AK-225")

    assert exit_code == 1
    assert payload["failed_step"] == "readiness"
    assert payload["steps"][1]["status"] == "skipped"
    smoke.assert_not_called()


def test_run_e2e_smoke_report_failure_points_to_report():
    patches = _patch_e2e_success()
    with patches[0], patches[1], \
         patch(
             "autoresearch.e2e.smoke.check_report_completeness",
             return_value=(1, {"ok": False, "missing": ["prometheus"]}),
         ), \
         patches[3] as archon:
        exit_code, payload = run_e2e_smoke(server="A2-AK-225")

    assert exit_code == 1
    assert payload["failed_step"] == "report"
    assert payload["steps"][2]["diagnosis"] == "missing: prometheus"
    archon.assert_not_called()


def test_run_e2e_smoke_archon_failure_skips_duration():
    patches = _patch_e2e_success()
    with patches[0], patches[1], patches[2], \
         patch("autoresearch.e2e.smoke._check_archon_observable", return_value=(1, {"ok": False, "error": "down"})):
        exit_code, payload = run_e2e_smoke(server="A2-AK-225")

    assert exit_code == 1
    assert payload["failed_step"] == "archon"
    assert payload["steps"][-1]["id"] == "duration"
    assert payload["steps"][-1]["status"] == "skipped"


def test_run_e2e_smoke_duration_failure():
    patches = _patch_e2e_success()
    with patches[0], patches[1], patches[2], patches[3]:
        exit_code, payload = run_e2e_smoke(server="A2-AK-225", max_duration=-1)

    assert exit_code == 1
    assert payload["failed_step"] == "duration"


def test_e2e_smoke_cli_outputs_single_json_object():
    runner = CliRunner()
    payload = {"ok": True, "command": "e2e-smoke", "run_id": "run123"}

    with patch("autoresearch.e2e.smoke.run_e2e_smoke", return_value=(0, payload)) as mock:
        result = runner.invoke(
            main,
            [
                "e2e",
                "smoke",
                "--server",
                "A2-AK-225",
                "--max-duration",
                "30",
                "--archon-url",
                "http://localhost:8088",
            ],
        )

    assert result.exit_code == 0
    assert json.loads(result.output) == payload
    assert mock.call_args.kwargs["server"] == "A2-AK-225"
    assert mock.call_args.kwargs["max_duration"] == 30.0
