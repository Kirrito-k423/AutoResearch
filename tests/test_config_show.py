"""Tests for autoresearch config show (CFG-SHOW-01)."""
import json
import pytest
from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.config.show import _is_sensitive, _redact


# === 脱敏函数 unit test ===

def test_is_sensitive_password_secret_token():
    assert _is_sensitive("password") is True
    assert _is_sensitive("Password") is True
    assert _is_sensitive("bootstrap_password_secret") is True
    assert _is_sensitive("api_token") is True
    assert _is_sensitive("credentials") is True


def test_is_sensitive_safe_fields():
    assert _is_sensitive("identity_file") is False
    assert _is_sensitive("name") is False
    assert _is_sensitive("host") is False
    assert _is_sensitive("user") is False
    assert _is_sensitive("keyring") is False


def test_redact_nested_dict():
    data = {
        "servers": [
            {"name": "n1", "bootstrap_password_secret": "opensesame"},
            {"name": "n2", "identity_file": "~/.ssh/id_ed25519"},
        ],
        "log": {"level": "INFO"},
    }
    out = _redact(data)
    assert out["servers"][0]["bootstrap_password_secret"] == "***"
    assert out["servers"][0]["name"] == "n1"
    assert out["servers"][1]["identity_file"] == "~/.ssh/id_ed25519"
    assert out["log"]["level"] == "INFO"


# === CLI 端到端 ===

def test_show_redacts_sensitive_fields(tmp_path, monkeypatch):
    """CFG-SHOW-01: 敏感字段值显示 ***."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "version: 1\n"
        "servers:\n"
        "  - name: srv\n"
        "    host: 192.0.2.1\n"
        "    port: 22\n"
        "    user: root\n"
        "    identity_file: ~/.ssh/id_ed25519\n"
        "    bootstrap_password_secret: super-secret-password\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 0
    out = result.output
    assert "super-secret-password" not in out
    assert "***" in out
    assert "~/.ssh/id_ed25519" in out


def test_show_json_output(tmp_path, monkeypatch):
    """D-07: --json 返 JSON (脱敏后)."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "version: 1\n"
        "servers:\n"
        "  - name: srv\n"
        "    host: h\n"
        "    port: 22\n"
        "    user: u\n"
        "    bootstrap_password_secret: plaintext-pw\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["servers"][0]["bootstrap_password_secret"] == "***"
    assert payload["servers"][0]["name"] == "srv"


def test_show_english_lang_no_chinese_token(tmp_path, monkeypatch):
    """D-07: --lang en 不含 '已脱敏' 中文 token."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text("version: 1\nservers: []\n", encoding="utf-8")
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show", "--lang", "en"])
    assert result.exit_code == 0
    assert "已脱敏" not in result.output
    assert "sensitive" in result.output.lower()


def test_show_missing_config_returns_1(tmp_path, monkeypatch):
    """不存在的 config → exit 1."""
    cfg = tmp_path / "nope.yaml"
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg))
    runner = CliRunner()
    result = runner.invoke(main, ["config", "show"])
    assert result.exit_code == 1
    combined = (result.output or "") + (result.stderr or "")
    assert "不存在" in combined or "失败" in combined or "❌" in combined
