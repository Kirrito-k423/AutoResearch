"""CLI contract tests for ``autoresearch hw probe``."""
from __future__ import annotations

import json

from click.testing import CliRunner

from autoresearch.cli import main
from workspace_core.config import ConfigError
from workspace_core.result import CheckResult, CheckSeverity


def _result(*, ok: bool, severity: CheckSeverity) -> CheckResult:
    return CheckResult(
        ok=ok,
        severity=severity,
        data={
            "server": {"name": "a2-test", "host": "192.0.2.10", "port": 22},
            "devices": [
                {
                    "id": 0,
                    "chip_id": 0,
                    "name": "Ascend 910B2",
                    "health": "OK",
                    "bus_id": "0000:81:00.0",
                    "memory_total_mib": 65536,
                    "memory_used_mib": 3467,
                    "temperature_c": 36,
                    "utilization_pct": 0,
                }
            ],
            "processes": [],
            "driver_versions": {
                "npu_smi": None,
                "driver": None,
                "package": None,
            },
            "warnings": [],
            "field_errors": [],
            "fallback": None,
            "raw_log_path": None,
        },
        message="done" if ok else "failed",
        error=None if ok else "probe failure",
    )


def test_hw_probe_help_lists_server_and_all_options():
    result = CliRunner().invoke(main, ["hw", "probe", "--help"])

    assert result.exit_code == 0
    assert "--server" in result.stdout
    assert "--config" in result.stdout
    assert "--lang" in result.stdout
    assert "--all" in result.stdout


def test_hw_probe_happy_path_outputs_one_json_and_progress(monkeypatch):
    from autoresearch.hw import probe as probe_module

    monkeypatch.setattr(
        probe_module,
        "probe_server",
        lambda server, config_path=None: _result(
            ok=True,
            severity=CheckSeverity.OK,
        ),
    )

    result = CliRunner().invoke(
        main,
        ["hw", "probe", "--server", "a2-test"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["severity"] == "ok"
    assert payload["data"]["devices"][0]["memory_total_mib"] == 65536
    assert "__AR_PROGRESS__=" in result.stderr
    assert "__AR_PROGRESS__=" not in result.stdout


def test_hw_probe_failure_returns_exit_one_and_json(monkeypatch):
    from autoresearch.hw import probe as probe_module

    monkeypatch.setattr(
        probe_module,
        "probe_server",
        lambda server, config_path=None: _result(
            ok=False,
            severity=CheckSeverity.FAIL,
        ),
    )

    result = CliRunner().invoke(
        main,
        ["hw", "probe", "--server", "a2-test", "--lang", "en"],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["severity"] == "fail"
    assert "probe failure" in result.stderr


def test_hw_probe_config_error_returns_exit_two_and_safe_json(monkeypatch):
    from autoresearch.hw import probe as probe_module

    def fail_config(server, config_path=None):
        raise ConfigError(f"unknown server: {server}")

    monkeypatch.setattr(probe_module, "probe_server", fail_config)

    result = CliRunner().invoke(
        main,
        ["hw", "probe", "--server", "missing"],
    )

    assert result.exit_code == 2
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["severity"] == "fail"
    assert payload["data"]["server"] == {"name": "missing"}
    serialized = result.stdout + result.stderr
    for sensitive_key in (
        "identity_file",
        "bootstrap_password_secret",
        "password",
        "private_key",
    ):
        assert sensitive_key not in serialized


def test_hw_probe_requires_exactly_one_target_mode():
    runner = CliRunner()

    missing = runner.invoke(main, ["hw", "probe"])
    conflicting = runner.invoke(
        main,
        ["hw", "probe", "--server", "a2-test", "--all"],
    )

    for result in (missing, conflicting):
        assert result.exit_code == 2
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert payload["severity"] == "fail"


def test_hw_monitor_help_lists_long_running_options():
    result = CliRunner().invoke(main, ["hw", "monitor", "--help"])

    assert result.exit_code == 0
    assert "--server" in result.stdout
    assert "--all" in result.stdout
    assert "--interval" in result.stdout
    assert "--duration" in result.stdout
    assert "--once" in result.stdout
    assert "--pushgateway-url" in result.stdout


def test_hw_monitor_cli_delegates_to_monitor_module(monkeypatch):
    from autoresearch.hw import monitor as monitor_module

    calls = []

    def fake_run_monitor(**kwargs):
        calls.append(kwargs)
        return 0

    monkeypatch.setattr(monitor_module, "run_monitor", fake_run_monitor)

    result = CliRunner().invoke(
        main,
        [
            "hw",
            "monitor",
            "--server",
            "a2-test",
            "--once",
            "--interval",
            "0.5",
            "--pushgateway-url",
            "http://push:9091",
        ],
    )

    assert result.exit_code == 0
    assert calls
    assert calls[0]["server"] == "a2-test"
    assert calls[0]["once"] is True
    assert calls[0]["interval_seconds"] == 0.5
    assert calls[0]["pushgateway_url"] == "http://push:9091"


def test_hw_probe_all_happy_path_outputs_one_json_and_progress(monkeypatch):
    from autoresearch.hw import probe as probe_module

    def fake_probe_all(config_path=None):
        for server_name in ("server-0", "server-1"):
            probe_module.emit_progress("hw.all.begin", server=server_name)
            probe_module.emit_progress("hw.all.complete", server=server_name)
        return CheckResult(
            ok=True,
            severity=CheckSeverity.WARN,
            data={
                "results": {
                    "server-0": _result(
                        ok=True,
                        severity=CheckSeverity.OK,
                    ),
                    "server-1": _result(
                        ok=True,
                        severity=CheckSeverity.WARN,
                    ),
                },
                "total": 2,
                "passed": 2,
                "failed": 0,
                "warned": 1,
                "passed_servers": ["server-0", "server-1"],
                "failed_servers": [],
            },
            message="done",
            error=None,
        )

    monkeypatch.setattr(probe_module, "probe_all", fake_probe_all)

    result = CliRunner().invoke(main, ["hw", "probe", "--all"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["severity"] == "warn"
    assert list(payload["data"]["results"]) == ["server-0", "server-1"]
    assert result.stdout.count("\n") == 1
    assert result.stderr.count('"stage": "hw.all.begin"') == 2
    assert result.stderr.count('"stage": "hw.all.complete"') == 2


def test_hw_probe_all_partial_failure_returns_exit_one(monkeypatch):
    from autoresearch.hw import probe as probe_module

    monkeypatch.setattr(
        probe_module,
        "probe_all",
        lambda config_path=None: CheckResult(
            ok=False,
            severity=CheckSeverity.FAIL,
            data={
                "results": {},
                "total": 2,
                "passed": 1,
                "failed": 1,
                "warned": 0,
                "passed_servers": ["server-0"],
                "failed_servers": ["server-1"],
            },
            message="partial failure",
            error="server-1 failed",
        ),
    )

    result = CliRunner().invoke(main, ["hw", "probe", "--all"])

    assert result.exit_code == 1
    assert json.loads(result.stdout)["ok"] is False
