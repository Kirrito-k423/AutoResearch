"""Tests for services.start / services.stop — focus on error paths."""
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.services.start import run_start
from autoresearch.services.stop import run_stop


def test_run_start_returns_2_when_docker_missing():
    """When docker CLI is missing, run_start should return 2 (and print Chinese error)."""
    with patch("autoresearch.services.start.shutil.which", return_value=None):
        code = run_start(lang="zh")
    assert code == 2


def test_run_stop_returns_2_when_docker_missing():
    with patch("autoresearch.services.stop.shutil.which", return_value=None):
        code = run_stop(lang="zh")
    assert code == 2


def test_start_help_does_not_crash():
    runner = CliRunner()
    result = runner.invoke(main, ["services", "start", "--help"])
    assert result.exit_code == 0


def test_stop_help_does_not_crash():
    runner = CliRunner()
    result = runner.invoke(main, ["services", "stop", "--help"])
    assert result.exit_code == 0
