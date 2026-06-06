"""Tests for SSHClient using paramiko dummy server (D-04c)."""
import socket
import threading
import time

import paramiko
import pytest

from workspace_core.ssh.client import SSHClient
from workspace_core.ssh.host import HostSpec, resolve_host
from workspace_core.ssh.exceptions import AuthError, ConnectError, HostResolveError


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def test_resolve_direct_form():
    h = resolve_host("user@example.com:2222")
    assert h.user == "user"
    assert h.host == "example.com"
    assert h.port == 2222
    assert h.alias is None


def test_resolve_direct_form_no_port():
    h = resolve_host("user@example.com")
    assert h.user == "user"
    assert h.host == "example.com"
    assert h.port == 22


def test_resolve_direct_form_invalid_port():
    with pytest.raises(HostResolveError):
        resolve_host("user@example.com:abc")


def test_resolve_direct_form_empty_user():
    with pytest.raises(HostResolveError):
        resolve_host("@example.com")


def test_resolve_unknown_alias_no_ssh_config(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    with pytest.raises(HostResolveError) as exc:
        resolve_host("nonexistent-alias-xyz")
    assert "ssh config" in str(exc.value) or "未找到" in str(exc.value)


def test_ssh_client_fails_to_connect_unknown_host():
    """Connect to a port that is unbound → ConnectError after retries."""
    h = HostSpec(alias=None, host="127.0.0.1", port=1, user="nobody", identity_file=None)  # port 1 unlikely
    c = SSHClient(h)
    with pytest.raises(ConnectError):
        c.connect(connect_timeout=0.3, retries=0)
