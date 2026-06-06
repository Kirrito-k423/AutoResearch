"""Tests for autoresearch ping CLI (D-18, D-19, D-20)."""
import json
import os
import socket
from pathlib import Path

import pytest
from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.ping import run_ping, _DummySSHServer


# === CLI 入口 ===

def test_ping_help_renders():
    runner = CliRunner()
    result = runner.invoke(main, ["ping", "--help"])
    assert result.exit_code == 0
    assert "--server" in result.stdout
    assert "--lang" in result.stdout


def test_ping_via_cli_no_args_runs_dummy():
    """D-18: autoresearch ping (无参) 走 dummy, exit 0 + JSON stdout.

    click 8.2+ CliRunner 默认分离 stdout / stderr, result.output = stdout.
    """
    runner = CliRunner()
    result = runner.invoke(main, ["ping"])
    assert result.exit_code == 0, f"unexpected exit; output={result.stdout!r} stderr={result.stderr!r}"
    payload = json.loads(result.stdout)
    assert payload["mode"] == "dummy"
    assert payload["ssh"] is True
    assert payload["reverse_tunnel"] is None  # dummy 跳过
    # 进度事件走 stderr (D-04d)
    assert "__AR_PROGRESS__=" in result.stderr


def test_ping_via_cli_english_lang():
    """--lang en 走通, output JSON 字段不变 (lang 只影响错误信息)."""
    runner = CliRunner()
    result = runner.invoke(main, ["ping", "--lang", "en"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["mode"] == "dummy"


# === run_ping 函数 (D-18 + D-20) ===

def test_ping_via_dummy_returns_zero_and_writes_json(capsys):
    """D-04e: stdout 唯一 JSON 对象."""
    exit_code = run_ping(server=None, lang="zh")
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert "ssh" in payload
    assert "reverse_tunnel" in payload
    assert "latency_ms" in payload
    assert payload["ssh"] is True
    assert payload["reverse_tunnel"] is None
    assert payload["mode"] == "dummy"
    assert isinstance(payload["latency_ms"], int)
    assert payload["latency_ms"] >= 0
    assert exit_code == 0


def test_ping_via_unknown_server_returns_2():
    """--server 但 config 找不到 → exit 2 + 错误信息含 server name."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["ping", "--server", "nonexistent-alias", "--lang", "zh"])
    assert result.exit_code == 2
    combined = (result.stdout or "") + (result.stderr or "")
    # 错误信息至少含 server name 或 "config" 关键词
    assert "nonexistent-alias" in combined or "config" in combined.lower()


# === _DummySSHServer 自身 ===

def test_dummy_ssh_server_context_manager_basic():
    """Dummy server context manager 自身工作正常, 端口监听."""
    with _DummySSHServer() as (host, stop):
        assert host.host == "127.0.0.1"
        assert host.port > 0
        assert host.user == "dummy"
        assert host.alias == "dummy"
        # 验证端口在监听
        s = socket.socket()
        try:
            s.settimeout(1.0)
            s.connect((host.host, host.port))
        finally:
            s.close()
    stop()  # idempotent 调


def test_dummy_ssh_server_echo_ok():
    """dummy server 跑 'echo ok' 应返 'ok' + exit 0."""
    from workspace_core.ssh.client import SSHClient
    with _DummySSHServer() as (host, _stop):
        with SSHClient(host) as c:
            c.connect()
            exit_code, out, err = c.exec("echo ok", timeout=5.0)
    assert exit_code == 0
    assert "ok" in out


def test_dummy_ssh_server_unknown_command_returns_nonzero():
    """dummy server 跑 'unknown' 应返非 0 + 'unknown' 文本."""
    from workspace_core.ssh.client import SSHClient
    with _DummySSHServer() as (host, _stop):
        with SSHClient(host) as c:
            c.connect()
            exit_code, out, err = c.exec("ls -la /", timeout=5.0)
    assert exit_code != 0
    assert "unknown" in out.lower()
