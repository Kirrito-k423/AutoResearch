"""Tests for network probe orchestration."""
from __future__ import annotations

from pathlib import Path
import threading
import time

import yaml

from autoresearch.net.curl import CURL_WRITE_OUT
from autoresearch.net.probe import (
    probe_all_remotes,
    probe_local,
    probe_remote_direct,
    summarize_rows,
)


DEFAULT_TARGETS = [
    "https://baidu.com",
    "https://huggingface.co",
    "https://github.com",
]


def _config(tmp_path: Path, count: int = 1) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "servers": [
                    {
                        "name": f"server-{index}",
                        "host": f"192.0.2.{index + 10}",
                        "port": 2222,
                        "user": "net-user",
                        "identity_file": "~/.ssh/id_net",
                        "bootstrap_password_secret": "test-secret",
                    }
                    for index in range(count)
                ],
                "network": {"targets": DEFAULT_TARGETS},
            }
        ),
        encoding="utf-8",
    )
    return path


def _stdout(code: int = 200, seconds: str = "0.100", speed: str = "1000") -> str:
    return (
        "\n__AR_CURL_BEGIN__\n"
        f"http_code={code}\n"
        f"time_total={seconds}\n"
        f"speed_download={speed}\n"
        "__AR_CURL_END__\n"
    )


class Completed:
    def __init__(self, returncode: int, stdout: str, stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FakeSSHClient:
    def __init__(self, host, *, bootstrap_password=None, fail_connect=False):
        self.host = host
        self.bootstrap_password = bootstrap_password
        self.fail_connect = fail_connect
        self.commands: list[str] = []
        self.closed = False
        self.connect_timeouts: list[float] = []

    def connect(self, *, connect_timeout: float) -> None:
        self.connect_timeouts.append(connect_timeout)
        if self.fail_connect:
            raise RuntimeError("connect failed")

    def exec(self, command: str):
        self.commands.append(command)
        return (0, _stdout(), "")

    def close(self) -> None:
        self.closed = True


def test_probe_local_default_targets_and_proxy_fallback():
    calls: list[list[str]] = []

    def fake_run(command, **kwargs):
        calls.append(command)
        url = command[-1]
        is_proxy = "--proxy" in command
        if "baidu" in url:
            return Completed(0, _stdout())
        if is_proxy:
            return Completed(0, _stdout(seconds="0.200", speed="2000"))
        return Completed(28, _stdout(code=0), "timeout")

    rows = probe_local(DEFAULT_TARGETS, run_cmd=fake_run)

    assert len(rows) == 3
    assert rows[0]["target_label"] == "baidu"
    assert rows[0]["status"] == "ok"
    for row in rows[1:]:
        assert row["status"] == "warn"
        assert row["effective_mode"] == "proxy"
        assert len(row["attempts"]) == 2
    assert len(calls) == 5


def test_probe_remote_direct_uses_safe_quoted_curl_and_closes_client(tmp_path):
    clients: list[FakeSSHClient] = []

    def factory(host, *, bootstrap_password=None):
        client = FakeSSHClient(host, bootstrap_password=bootstrap_password)
        clients.append(client)
        return client

    target = "https://github.com/search?q=hello&scope=repo"
    rows = probe_remote_direct(
        "server-0",
        [target],
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert rows[0]["status"] == "ok"
    assert rows[0]["server"] == "server-0"
    assert clients[0].host.identity_file == Path("~/.ssh/id_net").expanduser()
    assert clients[0].bootstrap_password == "test-secret"
    assert clients[0].connect_timeouts == [5.0]
    assert clients[0].closed is True
    command = clients[0].commands[0]
    assert "curl --max-time 10 -L -o /dev/null -s -w" in command
    assert "'https://github.com/search?q=hello&scope=repo'" in command
    assert CURL_WRITE_OUT.strip().splitlines()[0] in command


def test_probe_all_remotes_bounds_concurrency_and_preserves_config_order(
    tmp_path,
):
    lock = threading.Lock()
    active = 0
    max_active = 0
    completed: list[str] = []

    def fake_probe(server_name, targets, config_path):
        nonlocal active, max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep((5 - int(server_name.rsplit("-", 1)[1])) * 0.01)
        with lock:
            active -= 1
            completed.append(server_name)
        return [
            {
                "location": "remote",
                "server": server_name,
                "target_label": "baidu",
                "target_url": "https://baidu.com",
                "effective_mode": "direct",
                "status": "ok",
                "http_code": 200,
                "latency_ms": 10,
                "speed_download_bps": 100,
                "attempts": [],
                "error": None,
            }
        ]

    rows = probe_all_remotes(
        _config(tmp_path, count=5),
        ["https://baidu.com"],
        probe_fn=fake_probe,
        max_workers=9,
    )

    assert max_active <= 3
    assert len(completed) == 5
    assert completed != [f"server-{index}" for index in range(5)]
    assert [row["server"] for row in rows] == [
        f"server-{index}" for index in range(5)
    ]


def test_probe_all_remotes_converts_worker_exception_and_keeps_others(
    tmp_path,
):
    def fake_probe(server_name, targets, config_path):
        if server_name == "server-1":
            raise RuntimeError("isolated failure")
        return [
            {
                "location": "remote",
                "server": server_name,
                "target_label": "baidu",
                "target_url": "https://baidu.com",
                "effective_mode": "direct",
                "status": "ok",
                "http_code": 200,
                "latency_ms": 10,
                "speed_download_bps": 100,
                "attempts": [],
                "error": None,
            }
        ]

    rows = probe_all_remotes(
        _config(tmp_path, count=3),
        ["https://baidu.com"],
        probe_fn=fake_probe,
    )

    assert [row["server"] for row in rows] == [
        "server-0",
        "server-1",
        "server-2",
    ]
    failed = [row for row in rows if row["server"] == "server-1"][0]
    assert failed["status"] == "fail"
    assert "isolated failure" in failed["error"]


def test_summarize_rows_groups_local_remote_and_totals():
    rows = [
        {
            "location": "local",
            "server": None,
            "target_label": "baidu",
            "target_url": "https://baidu.com",
            "effective_mode": "direct",
            "status": "ok",
            "http_code": 200,
            "latency_ms": 10,
            "speed_download_bps": 100,
            "attempts": [],
            "error": None,
        },
        {
            "location": "remote",
            "server": "server-0",
            "target_label": "github",
            "target_url": "https://github.com",
            "effective_mode": "proxy",
            "status": "warn",
            "http_code": 200,
            "latency_ms": 20,
            "speed_download_bps": 200,
            "attempts": [],
            "error": None,
        },
        {
            "location": "remote",
            "server": "server-0",
            "target_label": "huggingface",
            "target_url": "https://huggingface.co",
            "effective_mode": None,
            "status": "fail",
            "http_code": None,
            "latency_ms": None,
            "speed_download_bps": None,
            "attempts": [],
            "error": "timeout",
        },
    ]

    summary = summarize_rows(rows)

    assert summary["total"] == 3
    assert summary["passed"] == 1
    assert summary["warned"] == 1
    assert summary["failed"] == 1
    assert summary["local"]["passed"] == 1
    assert summary["remotes"]["server-0"]["failed_targets"] == ["huggingface"]
    assert summary["needs_proxy"] is True
