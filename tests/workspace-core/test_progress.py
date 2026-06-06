"""Tests for progress emitter (D-14, D-15)."""
import json
import pytest

from workspace_core.progress import emit_progress, PROGRESS_PREFIX


def test_emit_progress_writes_to_stderr(capsys):
    emit_progress("test.stage", data={"k": "v"})
    captured = capsys.readouterr()
    assert captured.err.startswith(PROGRESS_PREFIX)
    payload = json.loads(captured.err[len(PROGRESS_PREFIX):])
    assert payload["stage"] == "test.stage"
    assert payload["data"] == {"k": "v"}
    assert payload["level"] == "info"
    assert "ts" in payload


def test_emit_progress_does_not_pollute_stdout(capsys):
    emit_progress("test")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_emit_progress_with_extra_fields(capsys):
    emit_progress("ssh.connect", host="nvidia-01", latency_ms=42)
    captured = capsys.readouterr()
    payload = json.loads(captured.err[len(PROGRESS_PREFIX):])
    assert payload["host"] == "nvidia-01"
    assert payload["latency_ms"] == 42


def test_emit_progress_chinese_in_data(capsys):
    emit_progress("test", data={"msg": "你好"})
    captured = capsys.readouterr()
    payload = json.loads(captured.err[len(PROGRESS_PREFIX):])
    assert payload["data"]["msg"] == "你好"


def test_emit_progress_warn_level(capsys):
    emit_progress("warn.test", level="warn")
    captured = capsys.readouterr()
    payload = json.loads(captured.err[len(PROGRESS_PREFIX):])
    assert payload["level"] == "warn"
