"""Tests for autoresearch.stack CLI group (Phase 07-01)."""
from unittest.mock import patch
from click.testing import CliRunner

from autoresearch.cli import main


def test_stack_help_does_not_crash():
    """autoresearch stack --help 列出 check 子命令."""
    runner = CliRunner()
    result = runner.invoke(main, ["stack", "--help"])
    assert result.exit_code == 0
    assert "check" in result.output


def test_stack_check_help_does_not_crash():
    """autoresearch stack check --help 列出选项."""
    runner = CliRunner()
    result = runner.invoke(main, ["stack", "check", "--help"])
    assert result.exit_code == 0
    assert "--server" in result.output
    assert "--all" in result.output
    assert "--lib" in result.output


def test_stack_check_mutually_exclusive_no_args():
    """既不传 --server 也不传 --all -> exit 2."""
    runner = CliRunner()
    result = runner.invoke(main, ["stack", "check"])
    assert result.exit_code == 2


def test_stack_check_mutually_exclusive_both_args(tmp_path):
    """--server + --all 同时传 -> exit 2."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "ok-srv", "host": "1.2.3.4", "user": "root", "conda_env": "verl-env"}],
    }))
    runner = CliRunner()
    result = runner.invoke(main, ["stack", "check", "--server", "ok-srv", "--all", "--config", str(cfg_path)])
    assert result.exit_code == 2


def test_stack_check_invokes_run_stack_check(tmp_path):
    """CLI -> run_stack_check 转发 server+config+libs."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "ok-srv", "host": "1.2.3.4", "user": "root"}],
    }))
    runner = CliRunner()
    with patch("autoresearch.stack.checker.run_stack_check") as m:
        m.return_value = 0
        result = runner.invoke(main, ["stack", "check", "--server", "ok-srv", "--config", str(cfg_path)])
    assert m.called
    # CLI 转发 server + config
    args, kwargs = m.call_args
    assert "ok-srv" in (args + tuple(kwargs.values()))
    assert result.exit_code == 0
