"""Tests for autoresearch.reach CLI group (Phase 06-02)."""
import json
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from autoresearch.cli import main


def test_reach_help_does_not_crash():
    """autoresearch reach --help 给出子命令列表."""
    runner = CliRunner()
    result = runner.invoke(main, ["reach", "--help"])
    assert result.exit_code == 0
    assert "test" in result.output


def test_reach_test_help_does_not_crash():
    """autoresearch reach test --help 列出选项."""
    runner = CliRunner()
    result = runner.invoke(main, ["reach", "test", "--help"])
    assert result.exit_code == 0
    assert "--server" in result.output
    assert "--lang" in result.output


def test_reach_test_missing_server_errors():
    """--server 必传, 不传 -> exit 2."""
    runner = CliRunner()
    result = runner.invoke(main, ["reach", "test"])
    assert result.exit_code != 0
    assert "Missing option" in result.output or "--server" in result.output


def test_reach_test_invokes_run_reach_test(tmp_path):
    """CLI -> run_reach_test 转发 server+config."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "ok-srv", "host": "1.2.3.4", "user": "root"}],
    }))
    runner = CliRunner()
    with patch("autoresearch.reach.tester.run_reach_test") as m:
        m.return_value = 0
        result = runner.invoke(main, ["reach", "test", "--server", "ok-srv", "--config", str(cfg_path)])
    assert m.called
    args, kwargs = m.call_args
    assert kwargs.get("server") == "ok-srv" or args[0] == "ok-srv"
    assert result.exit_code == 0


def test_reach_test_mutually_exclusive_no_args():
    """既不传 --server 也不传 --all -> exit 2."""
    runner = CliRunner()
    result = runner.invoke(main, ["reach", "test"])
    assert result.exit_code == 2
    assert "二选一" in result.output or "error" in result.output.lower()


def test_reach_test_mutually_exclusive_both_args(tmp_path):
    """--server + --all 同时传 -> exit 2."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "ok-srv", "host": "1.2.3.4", "user": "root"}],
    }))
    runner = CliRunner()
    result = runner.invoke(main, ["reach", "test", "--server", "ok-srv", "--all", "--config", str(cfg_path)])
    assert result.exit_code == 2


def test_reach_test_all_invokes_run_reach_test_all(tmp_path):
    """--all 走 run_reach_test_all."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [
            {"name": "s1", "host": "1.1.1.1", "user": "root"},
            {"name": "s2", "host": "2.2.2.2", "user": "root"},
        ],
    }))
    runner = CliRunner()
    with patch("autoresearch.reach.tester.run_reach_test_all") as m:
        m.return_value = 0
        result = runner.invoke(main, ["reach", "test", "--all", "--config", str(cfg_path)])
    assert m.called
    assert result.exit_code == 0
