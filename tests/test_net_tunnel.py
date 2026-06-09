"""Tests for network reverse tunnel state and ensure logic."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from autoresearch.net import tunnel as tunnel_module
from autoresearch.net.tunnel import (
    delete_tunnel_state,
    ensure_tunnel,
    load_tunnel_state,
    redact_proxy_url,
    state_path_for,
    write_tunnel_state,
)
from workspace_core.config import ConfigError
from workspace_core.ssh.exceptions import TunnelError
from workspace_core.ssh.tunnel import ReverseTunnel


@pytest.fixture(autouse=True)
def fake_tunnel_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(tunnel_module, "TUNNELS_DIR", tmp_path / "tunnels")
    monkeypatch.setattr(tunnel_module, "LOGS_DIR", tmp_path / "logs")
    return tmp_path


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "servers": [
                    {
                        "name": "server-0",
                        "host": "192.0.2.10",
                        "port": 2222,
                        "user": "net-user",
                        "identity_file": "~/.ssh/id_net",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _state(pid: int = 123):
    return {
        "server": "server-0",
        "pid": pid,
        "remote_port": 17890,
        "local_proxy_url": "http://127.0.0.1:7890",
        "remote_proxy_url": "http://127.0.0.1:17890",
        "started_at": "2026-06-09T00:00:00Z",
        "log_path": None,
        "last_heartbeat_at": "2026-06-09T00:00:00Z",
        "last_heartbeat_ok": True,
        "error": None,
    }


def _opener(pid: int = 456):
    calls: list[dict] = []

    def open_tunnel(host, *, remote_port, local_port, identity_file, log_dir):
        calls.append(
            {
                "host": host,
                "remote_port": remote_port,
                "local_port": local_port,
                "identity_file": identity_file,
                "log_dir": log_dir,
            }
        )
        return ReverseTunnel(
            proc=MagicMock(),
            pid=pid,
            host_alias=host.alias or host.host,
            remote_port=remote_port,
            local_port=local_port,
            log_path=log_dir / "tunnel.log",
        )

    return open_tunnel, calls


def test_redact_proxy_url_hides_userinfo():
    redacted = redact_proxy_url("http://u:p@127.0.0.1:7890")

    assert "u:p" not in redacted
    assert redacted == "http://***:***@127.0.0.1:7890"


def test_state_path_for_sanitizes_server_name():
    path = state_path_for("bad/name;server")

    assert path.name == "bad_name_server.json"
    assert "/" not in path.name
    assert ";" not in path.name


def test_state_roundtrip_redacts_sensitive_proxy_and_recovers_from_bad_json():
    state = _state()
    state["local_proxy_url"] = "http://u:p@127.0.0.1:7890"

    path = write_tunnel_state(state)
    text = path.read_text(encoding="utf-8")

    assert "u:p" not in text
    assert "identity_file" not in text
    assert "bootstrap_password_secret" not in text
    assert "password" not in text
    assert load_tunnel_state("server-0")["local_proxy_url"] == (
        "http://***:***@127.0.0.1:7890"
    )

    path.write_text("{broken", encoding="utf-8")
    assert load_tunnel_state("server-0") is None


def test_delete_tunnel_state_is_idempotent():
    write_tunnel_state(_state())
    delete_tunnel_state("server-0")
    delete_tunnel_state("server-0")

    assert load_tunnel_state("server-0") is None


def test_ensure_tunnel_opens_without_state_using_default_ports(tmp_path):
    opener, calls = _opener(pid=456)

    state = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        tunnel_opener=opener,
    )

    assert state["pid"] == 456
    assert state["remote_port"] == 17890
    assert state["remote_proxy_url"] == "http://127.0.0.1:17890"
    assert calls[0]["remote_port"] == 17890
    assert calls[0]["local_port"] == 7890
    assert calls[0]["identity_file"] == Path("~/.ssh/id_net").expanduser()


def test_ensure_tunnel_reuses_alive_state(monkeypatch, tmp_path):
    opener, calls = _opener(pid=456)
    write_tunnel_state(_state(pid=123))
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: True)

    state = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        tunnel_opener=opener,
    )

    assert state["pid"] == 123
    assert calls == []
    assert state["last_heartbeat_ok"] is True


def test_ensure_tunnel_rebuilds_dead_state(monkeypatch, tmp_path):
    opener, calls = _opener(pid=789)
    write_tunnel_state(_state(pid=123))
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: False)

    state = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        tunnel_opener=opener,
    )

    assert state["pid"] == 789
    assert len(calls) == 1


def test_ensure_tunnel_rejects_non_localhost_proxy(tmp_path):
    opener, _ = _opener()

    with pytest.raises(ConfigError):
        ensure_tunnel(
            "server-0",
            config_path=_config(tmp_path),
            local_proxy_url="http://proxy.example.com:7890",
            tunnel_opener=opener,
        )


def test_ensure_tunnel_start_error_is_bounded_and_redacted(tmp_path):
    def fail_open(*args, **kwargs):
        raise TunnelError("bad http://u:p@127.0.0.1:7890 " + ("x" * 800))

    with pytest.raises(TunnelError) as exc:
        ensure_tunnel(
            "server-0",
            config_path=_config(tmp_path),
            local_proxy_url="http://u:p@127.0.0.1:7890",
            tunnel_opener=fail_open,
        )

    message = str(exc.value)
    assert "u:p" not in message
    assert "http://***:***@127.0.0.1:7890" in message
    assert len(message) <= 500
