"""CLI smoke tests: --version, --help."""
from click.testing import CliRunner

from autoresearch.cli import main


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_help_shows_services():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "services" in result.output
    assert "check" in result.output
    assert "run" in result.output


def test_services_help_shows_subcommands():
    runner = CliRunner()
    result = runner.invoke(main, ["services", "--help"])
    assert result.exit_code == 0
    assert "status" in result.output
    assert "start" in result.output
    assert "stop" in result.output
