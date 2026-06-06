"""Tests for CheckResult schema (D-21)."""
import pytest

from workspace_core.result import ok, fail, merge, CheckResult, CheckSeverity


def test_ok_factory():
    r = ok(data={"x": 1}, message="done")
    assert r["ok"] is True
    assert r["severity"] == CheckSeverity.OK
    assert r["data"] == {"x": 1}
    assert r["error"] is None
    assert r["message"] == "done"


def test_ok_factory_default_data():
    r = ok()
    assert r["ok"] is True
    assert r["data"] == {}


def test_fail_factory():
    r = fail(error="connection refused", message="ssh connect failed")
    assert r["ok"] is False
    assert r["severity"] == CheckSeverity.FAIL
    assert r["error"] == "connection refused"
    assert r["message"] == "ssh connect failed"


def test_fail_with_warn_severity():
    r = fail(error="slow", message="degraded", severity=CheckSeverity.WARN)
    assert r["ok"] is False
    assert r["severity"] == CheckSeverity.WARN


def test_merge_all_ok():
    results = [ok(data={"a": 1}), ok(data={"b": 2})]
    merged = merge(results)
    assert merged["ok"] is True
    assert merged["severity"] == CheckSeverity.OK
    assert merged["error"] is None
    assert merged["data"]["count"] == 2
    assert merged["data"]["failed"] == 0


def test_merge_one_fail():
    results = [ok(), fail("oops"), ok()]
    merged = merge(results)
    assert merged["ok"] is False
    assert merged["severity"] == CheckSeverity.FAIL
    assert "oops" in merged["error"]
    assert merged["data"]["failed"] == 1
    assert merged["data"]["count"] == 3


def test_merge_warn_only():
    results = [
        ok(),
        fail("slow", severity=CheckSeverity.WARN),
        ok(),
    ]
    merged = merge(results)
    assert merged["ok"] is False
    assert merged["severity"] == CheckSeverity.WARN


def test_merge_empty():
    merged = merge([])
    assert merged["ok"] is True
    assert merged["data"]["count"] == 0
