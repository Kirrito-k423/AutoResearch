"""CLI contract tests for ``autoresearch net probe``."""
from __future__ import annotations

import json
from types import SimpleNamespace

from click.testing import CliRunner

from autoresearch.cli import main
from workspace_core.config import ConfigError
from workspace_core.result import CheckSeverity


def _config(targets=None):
    return SimpleNamespace(
        network=SimpleNamespace(targets=targets or ["https://baidu.com"])
    )


def _rows(status: str = "ok"):
    return [
        {
            "location": "local",
            "server": None,
            "target_label": "baidu",
            "target_url": "https://baidu.com",
            "effective_mode": "direct" if status != "fail" else None,
            "status": status,
            "http_code": 200 if status != "fail" else None,
            "latency_ms": 10 if status != "fail" else None,
            "speed_download_bps": 100 if status != "fail" else None,
            "attempts": [],
            "error": None if status != "fail" else "timeout",
        }
    ]


def test_net_probe_help_lists_expected_options():
    result = CliRunner().invoke(main, ["net", "probe", "--help"])

    assert result.exit_code == 0
    assert "--server" in result.stdout
    assert "--local-only" in result.stdout
    assert "--config" in result.stdout
    assert "--local-proxy-url" in result.stdout
    assert "--lang" in result.stdout


def test_net_probe_happy_path_outputs_one_json_and_progress(monkeypatch):
    from autoresearch.net import probe as probe_module

    monkeypatch.setattr(probe_module, "from_path", lambda config: _config())
    monkeypatch.setattr(
        probe_module,
        "_validated_targets",
        lambda targets: ["https://baidu.com"],
    )
    monkeypatch.setattr(
        probe_module,
        "probe_local",
        lambda targets, local_proxy_url: _rows("ok"),
    )
    monkeypatch.setattr(
        probe_module,
        "probe_all_remotes",
        lambda config, targets: [],
    )

    result = CliRunner().invoke(main, ["net", "probe"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["severity"] == "ok"
    assert isinstance(payload["data"]["rows"], list)
    assert "summary" in payload["data"]
    assert "__AR_PROGRESS__=" in result.stderr
    assert "__AR_PROGRESS__=" not in result.stdout
    assert result.stdout.count("\n") == 1


def test_net_probe_warn_only_exits_zero(monkeypatch):
    from autoresearch.net import probe as probe_module

    monkeypatch.setattr(
        probe_module,
        "from_path",
        lambda config: _config(["https://github.com"]),
    )
    monkeypatch.setattr(
        probe_module,
        "_validated_targets",
        lambda targets: ["https://github.com"],
    )
    monkeypatch.setattr(
        probe_module,
        "probe_local",
        lambda targets, local_proxy_url: _rows("warn"),
    )
    monkeypatch.setattr(probe_module, "probe_all_remotes", lambda *args: [])

    result = CliRunner().invoke(main, ["net", "probe"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["severity"] == CheckSeverity.WARN


def test_net_probe_network_fail_exits_one(monkeypatch):
    from autoresearch.net import probe as probe_module

    monkeypatch.setattr(probe_module, "from_path", lambda config: _config())
    monkeypatch.setattr(
        probe_module,
        "_validated_targets",
        lambda targets: ["https://baidu.com"],
    )
    monkeypatch.setattr(
        probe_module,
        "probe_local",
        lambda targets, local_proxy_url: _rows("fail"),
    )
    monkeypatch.setattr(probe_module, "probe_all_remotes", lambda *args: [])

    result = CliRunner().invoke(main, ["net", "probe", "--local-only"])

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["severity"] == "fail"


def test_net_probe_config_error_exits_two_and_redacts_sensitive_words(monkeypatch):
    from autoresearch.net import probe as probe_module

    def fail_config(config):
        raise ConfigError("bad config")

    monkeypatch.setattr(probe_module, "from_path", fail_config)

    result = CliRunner().invoke(main, ["net", "probe"])

    assert result.exit_code == 2
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["severity"] == "fail"
    serialized = result.stdout + result.stderr
    assert "__AR_PROGRESS__=" not in result.stdout
    for sensitive_key in (
        "identity_file",
        "bootstrap_password_secret",
        "password",
        "private_key",
    ):
        assert sensitive_key not in serialized
