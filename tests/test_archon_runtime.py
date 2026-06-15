"""Tests for Archon runtime adapters."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from autoresearch.archon import runtime


def _config(path: Path) -> Path:
    cfg = path / "config.yaml"
    cfg.write_text(
        """
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.13.225
    port: 22
    user: root
network:
  enabled: true
  targets:
    - https://www.baidu.com
log:
  level: INFO
wandb:
  enabled: true
  project: autoresearch-local
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return cfg


def test_build_env_uses_first_config_server(monkeypatch, tmp_path):
    cfg = _config(tmp_path)
    artifacts = tmp_path / "artifacts"
    monkeypatch.setenv("AR_CONFIG_PATH", str(cfg))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts))
    monkeypatch.delenv("AR_SERVER", raising=False)

    env = runtime.build_env()

    assert env.server == "A2-AK-225"
    assert env.config_path == str(cfg)
    assert env.lib == "verl"
    assert env.timeout == 60.0
    assert env.pushgateway_url == "http://127.0.0.1:17891"
    assert artifacts.exists()


def test_stack_state_processes_libs_with_summary(monkeypatch, tmp_path):
    cfg = _config(tmp_path)
    monkeypatch.setenv("AR_CONFIG_PATH", str(cfg))
    monkeypatch.setenv("ARTIFACTS_DIR", str(tmp_path / "artifacts"))
    monkeypatch.setenv("AR_STACK_LIBS", "verl,veomni")

    def fake_stack(*, server, config, libs, lang):
        assert server == "A2-AK-225"
        assert config == str(cfg)
        print(json.dumps({"ok": True, "lib": libs[0]}))
        return 0

    with patch("autoresearch.stack.checker.run_stack_check", side_effect=fake_stack):
        setup_code, _ = runtime.setup_stack_state()
        step_one_code, _ = runtime.run_stack_step()
        step_two_code, _ = runtime.run_stack_step()
        summary_code, summary = runtime.summarize_stack_state()

    assert setup_code == 0
    assert step_one_code == 0
    assert step_two_code == 0
    assert summary_code == 0
    assert summary["ok"] is True
    state = json.loads((tmp_path / "artifacts" / "stack-state.json").read_text())
    assert state["complete"] is True
    assert [item["lib"] for item in state["results"]] == ["verl", "veomni"]


def test_collect_to_report_handoff(monkeypatch, tmp_path):
    cfg = _config(tmp_path)
    artifacts = tmp_path / "artifacts"
    monkeypatch.setenv("AR_CONFIG_PATH", str(cfg))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts))
    monkeypatch.setenv("AR_COLLECT_MAX_ATTEMPTS", "1")
    monkeypatch.delenv("AR_RUN_ID", raising=False)

    def fake_collect(**kwargs):
        assert kwargs["server"] == "A2-AK-225"
        return 0, {"ok": True, "run_id": "run-123", "manifest": "/tmp/manifest.json"}

    def fake_render(*, run_id, open_report=False, runs_root=None):
        assert run_id == "run-123"
        return 0, {"ok": True, "run_id": run_id, "report": "/tmp/report.html", "opened": False}

    with patch("autoresearch.collect.cli.run_collect", side_effect=fake_collect):
        runtime.setup_collect_state()
        runtime.run_collect_step()
        collect_code, collect_summary = runtime.summarize_collect_state()

    with patch("autoresearch.report.cli.run_render", side_effect=fake_render):
        report_code, report = runtime.run_skill_08()

    assert collect_code == 0
    assert collect_summary["ok"] is True
    assert report_code == 0
    assert report["payload"]["run_id"] == "run-123"
    assert json.loads((artifacts / "collect-result.json").read_text())["run_id"] == "run-123"
    assert json.loads((artifacts / "report-result.json").read_text())["payload"]["report"] == "/tmp/report.html"


def test_services_skill_aggregates_start_and_status(monkeypatch, tmp_path):
    cfg = _config(tmp_path)
    monkeypatch.setenv("AR_CONFIG_PATH", str(cfg))
    monkeypatch.setenv("ARTIFACTS_DIR", str(tmp_path / "artifacts"))

    def fake_status(*, as_json, lang):
        assert as_json is True
        print(json.dumps({"summary": {"total": 5, "healthy": 5, "unhealthy": 0}}))
        return 0

    with patch("autoresearch.services.start.run_start", return_value=0), \
         patch("autoresearch.services.status.run_status", side_effect=fake_status):
        exit_code, result = runtime.run_skill_02()

    assert exit_code == 0
    assert result["ok"] is True
    assert result["payload"]["start_exit_code"] == 0
    assert result["payload"]["status"]["summary"]["healthy"] == 5
