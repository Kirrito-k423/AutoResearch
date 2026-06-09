"""Tests for pure network curl helpers."""
from __future__ import annotations

import pytest

from autoresearch.net.curl import (
    CURL_WRITE_OUT,
    build_curl_command,
    parse_curl_result,
    validate_target_url,
)


def _write_out(
    *,
    http_code: str = "200",
    time_total: str = "0.123",
    speed_download: str = "4567.8",
) -> str:
    return (
        "\n__AR_CURL_BEGIN__\n"
        f"http_code={http_code}\n"
        f"time_total={time_total}\n"
        f"speed_download={speed_download}\n"
        "__AR_CURL_END__\n"
    )


def test_validate_target_url_accepts_http_https_only():
    assert validate_target_url("https://github.com") == "https://github.com"
    assert validate_target_url("http://baidu.com") == "http://baidu.com"

    for value in (
        "",
        "file:///etc/passwd",
        "https://github.com\nwhoami",
        "https://github.com;whoami",
        "https://",
    ):
        with pytest.raises(ValueError):
            validate_target_url(value)


def test_build_curl_command_returns_subprocess_argv():
    command = build_curl_command("https://baidu.com")

    assert command[0] == "curl"
    for token in ("--max-time", "10", "-L", "-o", "/dev/null", "-s", "-w"):
        assert token in command
    assert CURL_WRITE_OUT in command
    assert command[-1] == "https://baidu.com"
    assert isinstance(command, list)


def test_build_curl_command_includes_proxy_when_requested():
    command = build_curl_command(
        "https://github.com",
        proxy_url="http://127.0.0.1:7890",
    )

    assert "--proxy" in command
    assert "http://127.0.0.1:7890" in command


def test_parse_successful_curl_write_out():
    attempt = parse_curl_result(
        0,
        _write_out(),
        "",
        "direct",
        "https://baidu.com",
    )

    assert attempt["ok"] is True
    assert attempt["http_code"] == 200
    assert attempt["latency_ms"] == 123
    assert attempt["speed_download_bps"] == 4567
    assert attempt["error"] is None


def test_parse_timeout_or_dns_failure_keeps_bounded_error():
    attempt = parse_curl_result(
        28,
        _write_out(http_code="000", time_total="10.000", speed_download="0"),
        "Could not resolve host: example" * 50,
        "direct",
        "https://github.com",
    )

    assert attempt["ok"] is False
    assert attempt["http_code"] == 0
    assert attempt["latency_ms"] == 10000
    assert "curl exit code 28" in attempt["error"]
    assert len(attempt["error"]) < 380


def test_parse_malformed_write_out_is_failure_not_exception():
    attempt = parse_curl_result(
        0,
        "html body without markers",
        "",
        "direct",
        "https://github.com",
    )

    assert attempt["ok"] is False
    assert attempt["http_code"] is None
    assert "write-out" in attempt["error"]
