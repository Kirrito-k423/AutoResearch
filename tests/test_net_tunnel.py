"""Tests for network reverse tunnel state and ensure logic."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from autoresearch.net import tunnel as tunnel_module
from autoresearch.net.tunnel import (
    delete_tunnel_state,
    ensure_tunnel,
    heartbeat_tunnel,
    load_tunnel_state,
    redact_proxy_url,
    run_tunnel_ensure,
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


def test_ensure_tunnel_different_ports_do_not_clobber_each_other(monkeypatch, tmp_path):
    opened: list[int] = []
    stopped: list[int] = []

    def opener(host, *, remote_port, local_port, identity_file, log_dir):
        opened.append(remote_port)
        return ReverseTunnel(
            proc=MagicMock(),
            pid=remote_port,
            host_alias=host.alias or host.host,
            remote_port=remote_port,
            local_port=local_port,
            log_path=log_dir / f"tunnel-{remote_port}.log",
        )

    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: True)
    monkeypatch.setattr(tunnel_module, "_stop_process", lambda pid, timeout_s=3.0: stopped.append(pid))

    state_proxy = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        remote_proxy_port=17892,
        tunnel_opener=opener,
        heartbeat_fn=lambda *args, **kwargs: True,
    )
    state_wandb = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        local_proxy_url="http://127.0.0.1:8080",
        remote_proxy_port=17890,
        tunnel_opener=opener,
        heartbeat_fn=lambda *args, **kwargs: True,
    )

    assert opened == [17892, 17890]
    assert stopped == []
    assert state_proxy["pid"] == 17892
    assert state_wandb["pid"] == 17890
    assert load_tunnel_state("server-0", remote_port=17892)["pid"] == 17892
    assert load_tunnel_state("server-0", remote_port=17890)["pid"] == 17890


def test_delete_tunnel_state_preserves_legacy_other_port_state():
    legacy_path = state_path_for("server-0")
    legacy_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_path.write_text(
        json.dumps(
            {
                **_state(pid=456),
                "remote_port": 17890,
                "remote_proxy_url": "http://127.0.0.1:17890",
            }
        ),
        encoding="utf-8",
    )

    delete_tunnel_state("server-0", remote_port=17892)

    assert legacy_path.exists() is False
    assert load_tunnel_state("server-0", remote_port=17890)["pid"] == 456


def test_stop_process_returns_after_sigterm_when_process_exits(monkeypatch):
    signals: list[tuple[int, int]] = []

    monkeypatch.setattr(
        tunnel_module.os,
        "kill",
        lambda pid, sig: signals.append((pid, sig)),
    )
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: False)

    tunnel_module._stop_process(123, timeout_s=1.0)

    assert signals == [(123, tunnel_module.signal.SIGTERM)]


def test_stop_process_kills_when_process_stays_alive(monkeypatch):
    signals: list[tuple[int, int]] = []

    monkeypatch.setattr(
        tunnel_module.os,
        "kill",
        lambda pid, sig: signals.append((pid, sig)),
    )

    tunnel_module._stop_process(123, timeout_s=0.0)

    assert signals == [
        (123, tunnel_module.signal.SIGTERM),
        (123, tunnel_module.signal.SIGKILL),
    ]


def test_ensure_tunnel_opens_without_state_using_default_ports(tmp_path):
    opener, calls = _opener(pid=456)

    state = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        tunnel_opener=opener,
        heartbeat_fn=lambda *args, **kwargs: True,
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
        heartbeat_fn=lambda *args, **kwargs: True,
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
        heartbeat_fn=lambda *args, **kwargs: True,
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
            max_retries=0,
        )

    message = str(exc.value)
    assert "u:p" not in message
    assert "http://***:***@127.0.0.1:7890" in message
    assert len(message) <= 500


def test_ensure_tunnel_cleans_stale_remote_forward_after_port_conflict(tmp_path):
    attempts: list[int] = []
    cleaned: list[tuple[str, int]] = []

    def opener(host, *, remote_port, local_port, identity_file, log_dir):
        attempts.append(remote_port)
        if len(attempts) == 1:
            raise TunnelError(
                "remote port forwarding failed for listen port 17890"
            )
        return ReverseTunnel(
            proc=MagicMock(),
            pid=567,
            host_alias=host.alias or host.host,
            remote_port=remote_port,
            local_port=local_port,
            log_path=log_dir / "tunnel.log",
        )

    def cleaner(server, host, remote_port):
        cleaned.append((server.name, remote_port))
        return True

    state = ensure_tunnel(
        "server-0",
        config_path=_config(tmp_path),
        tunnel_opener=opener,
        heartbeat_fn=lambda *args, **kwargs: True,
        sleep_fn=lambda delay: None,
        max_retries=1,
        remote_forward_cleaner=cleaner,
    )

    assert attempts == [17890, 17890]
    assert cleaned == [("server-0", 17890)]
    assert state["pid"] == 567
    assert state["last_heartbeat_ok"] is True


class FakeHeartbeatSSHClient:
    def __init__(self, host, *, bootstrap_password=None, response=(0, "", "")):
        self.host = host
        self.bootstrap_password = bootstrap_password
        self.response = response
        self.commands: list[str] = []
        self.closed = False

    def connect(self, *, connect_timeout: float) -> None:
        self.connect_timeout = connect_timeout

    def exec(self, command: str, *, timeout: float = 30.0):
        self.commands.append(command)
        return self.response

    def close(self) -> None:
        self.closed = True


def _curl_stdout(code: int = 200) -> str:
    return (
        "\n__AR_CURL_BEGIN__\n"
        f"http_code={code}\n"
        "time_total=0.050\n"
        "speed_download=1000\n"
        "__AR_CURL_END__\n"
    )


def test_heartbeat_dead_pid_skips_remote_curl(monkeypatch, tmp_path):
    calls = 0
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: False)

    def factory(*args, **kwargs):
        nonlocal calls
        calls += 1
        return FakeHeartbeatSSHClient(*args, **kwargs)

    assert heartbeat_tunnel(
        "server-0",
        _state(pid=123),
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    ) is False
    assert calls == 0


def test_heartbeat_alive_pid_runs_remote_proxy_curl(monkeypatch, tmp_path):
    clients: list[FakeHeartbeatSSHClient] = []
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: True)

    def factory(host, *, bootstrap_password=None):
        client = FakeHeartbeatSSHClient(
            host,
            bootstrap_password=bootstrap_password,
            response=(0, _curl_stdout(), ""),
        )
        clients.append(client)
        return client

    ok = heartbeat_tunnel(
        "server-0",
        _state(pid=123),
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert ok is True
    assert clients[0].closed is True
    assert clients[0].commands
    assert clients[0].commands[0].startswith(
        "ALL_PROXY=http://127.0.0.1:17890"
    )


def test_heartbeat_remote_proxy_curl_error_returns_false(monkeypatch, tmp_path):
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: True)

    ok = heartbeat_tunnel(
        "server-0",
        _state(pid=123),
        config_path=_config(tmp_path),
        ssh_client_factory=lambda host, *, bootstrap_password=None: FakeHeartbeatSSHClient(
            host,
            bootstrap_password=bootstrap_password,
            response=(28, _curl_stdout(code=0), "timeout"),
        ),
    )

    assert ok is False


def test_ensure_retries_with_capped_backoff(monkeypatch, tmp_path):
    opener, calls = _opener(pid=456)
    sleeps: list[int] = []
    monkeypatch.setattr(tunnel_module, "is_process_alive", lambda pid: True)

    with pytest.raises(TunnelError):
        ensure_tunnel(
            "server-0",
            config_path=_config(tmp_path),
            tunnel_opener=opener,
            heartbeat_fn=lambda *args, **kwargs: False,
            sleep_fn=lambda delay: sleeps.append(delay),
            max_retries=3,
        )

    assert len(calls) == 4
    assert sleeps == [1, 2, 4]
    state = load_tunnel_state("server-0")
    assert state["last_heartbeat_ok"] is False


def test_run_tunnel_ensure_outputs_json(monkeypatch, capsys):
    monkeypatch.setattr(
        tunnel_module,
        "ensure_tunnel",
        lambda *args, **kwargs: _state(pid=999),
    )

    exit_code = run_tunnel_ensure("server-0")

    assert exit_code == 0
    captured = capsys.readouterr()
    assert '"ok": true' in captured.out
    assert "__AR_PROGRESS__=" not in captured.out
    assert "__AR_PROGRESS__=" in captured.err
