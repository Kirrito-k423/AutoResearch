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

# === D-04 fix: --lang en 切英文错误 (start/stop 缺 docker 时) ===

def test_start_missing_docker_lang_en_returns_english_error():
    """D-04: --lang en 切英文错误 (start)."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["services", "start", "--lang", "en"],
            env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"},
        )
    assert result.exit_code == 2
    combined = (result.output or "") + (result.stderr or "")
    assert "Error" in combined or "docker" in combined.lower()
    # 关键断言: 默认中文 "错误" 不应在 combined 里
    assert "错误" not in combined


def test_stop_missing_docker_lang_en_returns_english_error():
    """D-04: --lang en 切英文错误 (stop)."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["services", "stop", "--lang", "en"],
            env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"},
        )
    assert result.exit_code == 2
    combined = (result.output or "") + (result.stderr or "")
    assert "Error" in combined or "docker" in combined.lower()
    assert "错误" not in combined
