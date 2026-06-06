"""Tests for log formatters + get_logger (D-16)."""
import json
import logging
import pytest

from workspace_core.log.formatter import HumanFormatter, JsonFormatter
from workspace_core.log import get_logger, configure_root


def test_human_formatter_includes_level_and_msg():
    rec = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="hello %s", args=("world",), exc_info=None,
    )
    out = HumanFormatter().format(rec)
    assert "INFO" in out
    assert "test" in out
    assert "hello world" in out


def test_human_formatter_includes_ctx():
    rec = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="hello", args=(), exc_info=None,
    )
    rec.ctx = {"a": 1}
    out = HumanFormatter().format(rec)
    assert "ctx" in out
    assert "'a': 1" in out or '"a": 1' in out


def test_json_formatter_includes_required_fields():
    rec = logging.LogRecord(
        name="test", level=logging.WARNING, pathname="", lineno=0,
        msg="warn %d", args=(42,), exc_info=None,
    )
    rec.host = "nvidia-01"
    out = JsonFormatter().format(rec)
    payload = json.loads(out)
    assert payload["level"] == "WARNING"
    assert payload["logger"] == "test"
    assert payload["msg"] == "warn 42"
    assert payload["host"] == "nvidia-01"
    assert "ts" in payload


def test_json_formatter_omits_optional_when_missing():
    rec = logging.LogRecord(
        name="t", level=logging.INFO, pathname="", lineno=0,
        msg="hi", args=(), exc_info=None,
    )
    out = JsonFormatter().format(rec)
    payload = json.loads(out)
    assert "host" not in payload
    assert "ctx" not in payload
    assert "exc" not in payload


def test_get_logger_caches():
    a = get_logger("foo")
    b = get_logger("foo")
    assert a is b
    c = get_logger("bar")
    assert a is not c


def test_configure_root_writes_to_file(tmp_path):
    log_file = tmp_path / "subdir" / "app.log"
    configure_root(level=logging.INFO, log_file=log_file, enable_stderr=False)
    log = get_logger("test.config")
    log.info("hello %s", "world")
    log.warning("warn %d", 42)
    contents = log_file.read_text(encoding="utf-8")
    lines = [l for l in contents.strip().split("\n") if l]
    assert len(lines) == 2
    payload0 = json.loads(lines[0])
    assert payload0["level"] == "INFO"
    assert payload0["msg"] == "hello world"
    payload1 = json.loads(lines[1])
    assert payload1["level"] == "WARNING"
    assert payload1["msg"] == "warn 42"


def test_configure_root_is_idempotent(capsys):
    """多次 configure_root 不会堆 handler (复测时不互相污染)."""
    configure_root(level=logging.INFO, enable_stderr=True)
    root1 = logging.getLogger()
    n1 = len(root1.handlers)
    configure_root(level=logging.INFO, enable_stderr=True)
    n2 = len(root1.handlers)
    assert n1 == n2
