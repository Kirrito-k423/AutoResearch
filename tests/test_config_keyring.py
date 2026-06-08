"""Tests for autoresearch config keyring CLI."""
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from autoresearch.cli import main
from autoresearch.config import run_keyring
from workspace_core.secrets import KEYRING_AVAILABLE


# === run_keyring function unit test (mocked) ===

def test_keyring_set_get_mocked():
    """用 mock keyring 测 set/get."""
    mock_kr = MagicMock()
    mock_kr.get_password.return_value = "the-value"
    with patch("autoresearch.config.keyring_cli._backend_or_die", return_value=mock_kr):
        # set
        rc = run_keyring(action="set", name="FOO", value="bar", lang="zh")
        assert rc == 0
        mock_kr.set_password.assert_called_once_with("autoresearch", "FOO", "bar")
        # get
        rc = run_keyring(action="get", name="FOO", lang="zh")
        assert rc == 0
        mock_kr.get_password.assert_called_with("autoresearch", "FOO")


def test_keyring_get_missing_returns_1():
    mock_kr = MagicMock()
    mock_kr.get_password.return_value = None
    with patch("autoresearch.config.keyring_cli._backend_or_die", return_value=mock_kr):
        rc = run_keyring(action="get", name="MISSING", lang="zh")
    assert rc == 1


def test_keyring_delete_not_found_returns_1():
    mock_kr = MagicMock()
    err_cls = getattr(__import__("keyring").errors, "PasswordDeleteError", Exception)
    mock_kr.delete_password.side_effect = err_cls("not found")
    with patch("autoresearch.config.keyring_cli._backend_or_die", return_value=mock_kr):
        rc = run_keyring(action="delete", name="NOPE", lang="zh")
    assert rc == 1


def test_keyring_unavailable_returns_2():
    """keyring 不可用 → exit 2 + 中文错误."""
    with patch("autoresearch.config.keyring_cli._backend_or_die", return_value=None):
        rc = run_keyring(action="set", name="X", value="y", lang="zh")
    assert rc == 2


def test_keyring_set_requires_value():
    """set 没 --value → 中文错误 exit 1."""
    mock_kr = MagicMock()
    with patch("autoresearch.config.keyring_cli._backend_or_die", return_value=mock_kr):
        rc = run_keyring(action="set", name="X", value=None, lang="zh")
    assert rc == 1
    mock_kr.set_password.assert_not_called()


# === CLI 端到端 ===

def test_keyring_cli_help_renders():
    """CLI: autoresearch config keyring --help 列出 4 子命令."""
    runner = CliRunner()
    result = runner.invoke(main, ["config", "keyring", "--help"])
    assert result.exit_code == 0
    for sub in ["set", "get", "delete", "list"]:
        assert sub in result.output


def test_keyring_set_via_cli_mocked(monkeypatch):
    """CLI: autoresearch config keyring set NAME --value X."""
    mock_kr = MagicMock()
    monkeypatch.setattr(
        "autoresearch.config.keyring_cli._backend_or_die", lambda lang: mock_kr
    )
    runner = CliRunner()
    result = runner.invoke(
        main, ["config", "keyring", "set", "FOO", "--value", "bar"]
    )
    assert result.exit_code == 0
    mock_kr.set_password.assert_called_once_with("autoresearch", "FOO", "bar")


def test_keyring_get_via_cli_shows_value(monkeypatch):
    """CLI: get NAME 打印 value."""
    mock_kr = MagicMock()
    mock_kr.get_password.return_value = "the-secret"
    monkeypatch.setattr(
        "autoresearch.config.keyring_cli._backend_or_die", lambda lang: mock_kr
    )
    runner = CliRunner()
    result = runner.invoke(main, ["config", "keyring", "get", "FOO"])
    assert result.exit_code == 0
    assert "the-secret" in result.output
