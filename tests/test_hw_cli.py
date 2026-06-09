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


def test_hw_probe_help_lists_single_server_options():
    result = CliRunner().invoke(main, ["hw", "probe", "--help"])

    assert result.exit_code == 0
    assert "--server" in result.stdout
    assert "--config" in result.stdout
    assert "--lang" in result.stdout
    assert "--all" not in result.stdout


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
