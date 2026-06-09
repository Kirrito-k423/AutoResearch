"""Tests for single-server hardware probe orchestration."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from autoresearch.hw.probe import (
    NPU_SMI_INFO_COMMAND,
    probe_server,
    resolve_server_host,
)
from workspace_core.config import ConfigError
from workspace_core.result import CheckSeverity
from workspace_core.ssh import ConnectError


FIXTURES = Path(__file__).parent / "fixtures" / "hw"
BASELINE = (FIXTURES / "npu_smi_25_3_rc1_no_processes.txt").read_text(
    encoding="utf-8"
)
PARTIAL = (FIXTURES / "npu_smi_missing_metric.txt").read_text(
    encoding="utf-8"
)


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "servers": [
                    {
                        "name": "a2-test",
                        "host": "192.0.2.10",
                        "port": 2222,
                        "user": "hardware-user",
                        "identity_file": "~/.ssh/id_hardware",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


class FakeSSHClient:
    def __init__(
        self,
        host,
        *,
        response: tuple[int, str, str],
        connect_error: Exception | None = None,
    ) -> None:
        self.host = host
        self.response = response
        self.connect_error = connect_error
        self.connect_timeouts: list[float] = []
        self.commands: list[str] = []
        self.closed = False

    def connect(self, *, connect_timeout: float) -> None:
        self.connect_timeouts.append(connect_timeout)
        if self.connect_error is not None:
            raise self.connect_error

    def exec(self, command: str):
        self.commands.append(command)
        return self.response

    def close(self) -> None:
        self.closed = True


def _factory(
    *,
    response: tuple[int, str, str] = (0, BASELINE, ""),
    connect_error: Exception | None = None,
):
    clients: list[FakeSSHClient] = []

    def create(host):
        client = FakeSSHClient(
            host,
            response=response,
            connect_error=connect_error,
        )
        clients.append(client)
        return client

    return create, clients


def test_single_server_happy_path_uses_only_fixed_command(tmp_path):
    factory, clients = _factory()

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is True
    assert result["severity"] == CheckSeverity.OK
    assert len(result["data"]["devices"]) == 8
    assert clients[0].commands == [NPU_SMI_INFO_COMMAND]
    assert clients[0].connect_timeouts == [5.0]
    assert clients[0].closed is True
    assert set(result["data"]["server"]) == {"name", "host", "port"}


def test_timeout_becomes_fail_without_config_secrets(tmp_path):
    factory, clients = _factory(
        connect_error=ConnectError("timed out"),
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["severity"] == CheckSeverity.FAIL
    assert "connection failed" in result["error"]
    serialized = repr(result)
    assert "hardware-user" not in serialized
    assert "id_hardware" not in serialized
    assert "bootstrap_password_secret" not in serialized
    assert clients[0].commands == []
    assert clients[0].closed is True


def test_partial_core_metrics_fail_but_preserve_device_data(tmp_path):
    factory, clients = _factory(response=(0, PARTIAL, ""))

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["severity"] == CheckSeverity.FAIL
    device = result["data"]["devices"][0]
    assert device["memory_used_mib"] == 3467
    assert device["memory_total_mib"] is None
    assert device["bus_id"] == "0000:81:00.0"
    assert result["data"]["field_errors"]
    assert clients[0].closed is True


def test_command_nonzero_returns_exit_domain_failure(tmp_path):
    factory, clients = _factory(
        response=(9, BASELINE, "device manager unavailable"),
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["severity"] == CheckSeverity.FAIL
    assert "exit code 9" in result["error"]
    assert len(result["data"]["devices"]) == 8
    assert clients[0].closed is True


def test_unknown_server_fails_before_client_creation(tmp_path):
    factory, clients = _factory()

    with pytest.raises(ConfigError, match="missing-server"):
        resolve_server_host("missing-server", _config(tmp_path))

    assert clients == []
