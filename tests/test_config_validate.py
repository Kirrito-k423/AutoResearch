"""Tests for autoresearch config validate (CFG-VAL-01..02)."""
import json
import pytest
from click.testing import CliRunner

from autoresearch.cli import main


def test_validate_passes_on_minimal_config(tmp_path, monkeypatch):
    """CFG-VAL-01: 合法 config 校验通过."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text("version: 1\nservers: []\n", encoding="utf-8")
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "validate"])
    assert result.exit_code == 0
    assert "✅" in result.output
    assert "校验通过" in result.output


def test_validate_fails_with_chinese_error_on_missing_field(tmp_path, monkeypatch):
    """CFG-VAL-02: 失败指出具体字段 (中文)."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text("servers:\n  - {host: h, user: u}\n", encoding="utf-8")
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "validate"])
    assert result.exit_code == 1
    combined = (result.output or "") + (result.stderr or "")
    assert "name" in combined
    # 沉淀层 (workspace_core.config) 中文错误, 至少出现 "必填" 或 "配置"
    assert "必填" in combined or "配置" in combined


def test_validate_json_output(tmp_path, monkeypatch):
    """D-07: --json 返 JSON."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text("version: 1\nservers: []\n", encoding="utf-8")
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "validate", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert "summary" in payload
    assert payload["summary"]["version"] == 1
    assert payload["summary"]["servers_count"] == 0


def test_validate_en_lang_uses_english_top_line(tmp_path, monkeypatch):
    """D-07: --lang en 切 validate 自己的 header (✅ 校验通过 → ✅ validated)."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text("version: 1\nservers: []\n", encoding="utf-8")
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "validate", "--lang", "en"])
    assert result.exit_code == 0
    # validate 自己的英文文案
    assert "validated" in result.output
    # 中文 header "校验通过" 不应在
    assert "校验通过" not in result.output
