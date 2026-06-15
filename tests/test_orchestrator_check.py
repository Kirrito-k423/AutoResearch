"""Tests for `autoresearch check all` orchestration."""
from __future__ import annotations

import json
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.orchestrator.checks import run_check_all


def _fake_json(payload: dict, exit_code: int = 0):
    def inner(*args, **kwargs):
        print(json.dumps(payload, ensure_ascii=False))
        return exit_code

    return inner


def _patch_success_steps():
    return (
        patch("autoresearch.orchestrator.checks.run_validate", _fake_json({"ok": True})),
        patch(
            "autoresearch.orchestrator.checks.run_status",
            _fake_json({"summary": {"total": 5, "healthy": 5, "unhealthy": 0}}),
        ),
        patch("autoresearch.orchestrator.checks.run_hw_probe", _fake_json({"ok": True})),
        patch("autoresearch.orchestrator.checks.run_net_probe", _fake_json({"ok": True})),
        patch("autoresearch.orchestrator.checks.run_reach_test", _fake_json({"ok": True})),
        patch("autoresearch.orchestrator.checks.run_stack_check", _fake_json({"ok": True})),
    )


def test_run_check_all_happy_path_chains_eight_steps():
    patches = _patch_success_steps()
    with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5]:
        exit_code, payload = run_check_all(server="A2-AK-225", stack_libs=("verl",))

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["failed_step"] is None
    assert [step["id"] for step in payload["steps"]] == [
        "config",
        "services",
        "hw",
        "net",
        "reach",
        "stack",
        "collect",
        "report",
    ]
    assert payload["summary"]["passed"] == 8
    assert payload["steps"][6]["payload"]["message"].startswith("`run smoke`")


def test_run_check_all_reports_failed_step_and_skips_collect_report():
    patches = _patch_success_steps()
    unhealthy_status = _fake_json(
        {"summary": {"total": 5, "healthy": 4, "unhealthy": 1}},
        exit_code=1,
    )

    with patches[0], \
         patch("autoresearch.orchestrator.checks.run_status", unhealthy_status), \
         patches[2], patches[3], patches[4], patches[5]:
        exit_code, payload = run_check_all(server="A2-AK-225", stack_libs=("verl",))

    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["failed_step"] == "services"
    services_step = next(step for step in payload["steps"] if step["id"] == "services")
    assert services_step["diagnosis"] == "1 service(s) unhealthy"
    assert payload["steps"][-2]["status"] == "skipped"
    assert payload["steps"][-1]["status"] == "skipped"


def test_check_all_cli_outputs_single_json_object():
    runner = CliRunner()
    payload = {"ok": True, "command": "check", "summary": {"total": 8}}

    with patch("autoresearch.orchestrator.checks.run_check_all", return_value=(0, payload)) as mock:
        result = runner.invoke(
            main,
            [
                "check",
                "all",
                "--server",
                "A2-AK-225",
                "--stack-lib",
                "verl",
                "--remote-proxy-port",
                "18000",
            ],
        )

    assert result.exit_code == 0
    assert json.loads(result.output) == payload
    assert mock.call_args.kwargs["server"] == "A2-AK-225"
    assert mock.call_args.kwargs["stack_libs"] == ("verl",)
    assert mock.call_args.kwargs["remote_proxy_port"] == 18000
