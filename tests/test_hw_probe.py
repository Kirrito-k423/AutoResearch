"""Tests for single-server hardware probe orchestration."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from autoresearch.hw.probe import (
    DRIVER_VERSION_COMMAND,
    LSPCI_COMMAND,
    NPU_SMI_INFO_COMMAND,
    probe_server,
    resolve_server_host,
    typed_query_command,
    write_raw_failure_log,
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
UNKNOWN = (FIXTURES / "npu_smi_unknown_format.txt").read_text(encoding="utf-8")
DRIVER = (FIXTURES / "driver_version_info.txt").read_text(encoding="utf-8")
LSPCI = (FIXTURES / "lspci_ascend.txt").read_text(encoding="utf-8")


@pytest.fixture(autouse=True)
def local_failure_logs(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    monkeypatch.setattr("autoresearch.hw.probe.LOGS_DIR", logs_dir)
    return logs_dir


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
        responses: dict[str, tuple[int, str, str]] | None = None,
        connect_error: Exception | None = None,
    ) -> None:
        self.host = host
        self.response = response
        self.responses = responses or {}
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
        return self.responses.get(command, self.response)

    def close(self) -> None:
        self.closed = True


def _factory(
    *,
    response: tuple[int, str, str] = (0, BASELINE, ""),
    responses: dict[str, tuple[int, str, str]] | None = None,
    connect_error: Exception | None = None,
):
    clients: list[FakeSSHClient] = []
    command_responses = {
        DRIVER_VERSION_COMMAND: (0, DRIVER, ""),
        **(responses or {}),
    }

    def create(host):
        client = FakeSSHClient(
            host,
            response=response,
            responses=command_responses,
            connect_error=connect_error,
        )
        clients.append(client)
        return client

    return create, clients


def test_single_server_happy_path_uses_only_fixed_commands(tmp_path):
    factory, clients = _factory()

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is True
    assert result["severity"] == CheckSeverity.OK
    assert len(result["data"]["devices"]) == 8
    assert clients[0].commands == [
        NPU_SMI_INFO_COMMAND,
        DRIVER_VERSION_COMMAND,
    ]
    assert clients[0].connect_timeouts == [5.0]
    assert clients[0].closed is True
    assert set(result["data"]["server"]) == {"name", "host", "port"}
    assert result["data"]["raw_log_path"] is None
    assert result["data"]["raw_output_summary"] is None
    assert not (tmp_path / "logs").exists()


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


@pytest.mark.parametrize(
    ("metric_type", "device_id"),
    [
        ("shell", 0),
        ("temp", "0"),
        ("temp", -1),
        ("temp", True),
    ],
)
def test_typed_command_rejects_non_allowlisted_or_non_integer_input(
    metric_type,
    device_id,
):
    with pytest.raises(ValueError):
        typed_query_command(metric_type, device_id)


def test_typed_queries_fill_only_missing_values_with_integer_ids(tmp_path):
    factory, clients = _factory(
        response=(0, PARTIAL, ""),
        responses={
            "npu-smi info -t memory -i 0": (
                0,
                "| NPU ID | Memory Usage (MiB) |\n| 0 | 9999 / 65536 |\n",
                "",
            ),
            "npu-smi info -t temp -i 0": (
                0,
                "| Device ID | Temperature (C) |\n| 0 | 43 |\n",
                "",
            ),
            "npu-smi info -t usages -i 0": (
                0,
                "| ID | AI Core Usage (%) |\n| 0 | 20 |\n",
                "",
            ),
        },
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    device = result["data"]["devices"][0]
    assert result["ok"] is True
    assert result["severity"] == CheckSeverity.WARN
    assert device["memory_used_mib"] == 3467
    assert device["memory_total_mib"] == 65536
    assert device["temperature_c"] == 43
    assert device["utilization_pct"] == 20
    assert result["data"]["field_errors"] == []
    typed_commands = [
        command
        for command in clients[0].commands
        if command.startswith("npu-smi info -t ")
    ]
    assert all(
        command.rsplit(" ", 1)[-1].isdigit()
        for command in typed_commands
    )
    assert len(typed_commands) == 3
    assert any("conflict" in warning for warning in result["data"]["warnings"])
    assert any(
        "typed supplement used" in warning
        for warning in result["data"]["warnings"]
    )


def test_typed_query_nonzero_preserves_primary_values_and_warns(tmp_path):
    factory, clients = _factory(
        response=(0, PARTIAL, ""),
        responses={
            "npu-smi info -t memory -i 0": (8, "", "not supported"),
            "npu-smi info -t temp -i 0": (8, "", "not supported"),
            "npu-smi info -t usages -i 0": (8, "", "not supported"),
        },
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["data"]["devices"][0]["memory_used_mib"] == 3467
    assert len(
        [
            warning
            for warning in result["data"]["warnings"]
            if "exit code 8" in warning
        ]
    ) == 3
    assert clients[0].closed is True


def test_unknown_output_falls_back_to_lspci_and_remains_fail(tmp_path):
    long_unknown = UNKNOWN + ("未知格式诊断" * 200)
    factory, clients = _factory(
        response=(0, long_unknown, ""),
        responses={LSPCI_COMMAND: (0, LSPCI, "")},
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["severity"] == CheckSeverity.FAIL
    assert result["data"]["fallback"] == "lspci"
    assert len(result["data"]["devices"]) == 2
    assert clients[0].commands[-1] == LSPCI_COMMAND
    assert {
        error["field"] for error in result["data"]["field_errors"]
    } == {
        "memory_total_mib",
        "memory_used_mib",
        "temperature_c",
        "utilization_pct",
    }
    assert all(
        device[field] is None
        for device in result["data"]["devices"]
        for field in (
            "memory_total_mib",
            "memory_used_mib",
            "temperature_c",
            "utilization_pct",
        )
    )
    assert Path(result["data"]["raw_log_path"]).is_file()
    assert len(result["data"]["raw_output_summary"]) == 512
    assert "component=driver" not in result["data"]["raw_output_summary"]
    assert "parse failed" in result["error"]


def test_driver_versions_merge_header_and_fixed_read_only_file(tmp_path):
    factory, clients = _factory()

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert clients[0].commands[-1] == (
        "cat /usr/local/Ascend/driver/version.info"
    )
    assert result["data"]["driver_versions"] == {
        "npu_smi": "25.3.rc1",
        "driver": "25.3.rc1",
        "package": "25.3.rc1",
    }
    serialized = repr(result)
    assert "component=driver" not in serialized
    assert "build_time=" not in serialized


def test_missing_driver_file_warns_without_failing_complete_core_metrics(
    tmp_path,
):
    factory, _ = _factory(
        responses={
            DRIVER_VERSION_COMMAND: (1, "", "No such file or directory"),
        }
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is True
    assert result["severity"] == CheckSeverity.WARN
    assert result["data"]["driver_versions"] == {
        "npu_smi": "25.3.rc1",
        "driver": None,
        "package": None,
    }
    assert "build_time" not in repr(result)
    assert any(
        "version.info unavailable" in warning
        for warning in result["data"]["warnings"]
    )


def test_raw_log_sanitizes_name_and_preserves_full_output(
    tmp_path,
):
    raw = "诊断输出" + ("x" * 800)
    path = write_raw_failure_log(
        "bad/name;server",
        [
            {
                "command": NPU_SMI_INFO_COMMAND,
                "exit_code": 1,
                "stdout": raw,
                "stderr": "command failed",
            }
        ],
    )

    assert path.parent == tmp_path / "logs"
    assert path.name.startswith("hw-bad_name_server-")
    content = path.read_text(encoding="utf-8")
    assert raw in content
    assert "exit_code=1" in content


def test_nonzero_unknown_npu_smi_uses_lspci_fallback(tmp_path):
    factory, clients = _factory(
        response=(127, "", "npu-smi: command not found"),
        responses={LSPCI_COMMAND: (0, LSPCI, "")},
    )

    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["severity"] == CheckSeverity.FAIL
    assert result["data"]["fallback"] == "lspci"
    assert len(result["data"]["devices"]) == 2
    assert clients[0].commands[-1] == LSPCI_COMMAND


def test_raw_log_write_error_preserves_original_failure(
    tmp_path,
    monkeypatch,
):
    factory, _ = _factory(
        response=(0, UNKNOWN, ""),
        responses={LSPCI_COMMAND: (0, LSPCI, "")},
    )

    def fail_write(*args, **kwargs):
        raise OSError("read-only filesystem")

    monkeypatch.setattr(
        "autoresearch.hw.probe.write_raw_failure_log",
        fail_write,
    )
    result = probe_server(
        "a2-test",
        config_path=_config(tmp_path),
        ssh_client_factory=factory,
    )

    assert result["ok"] is False
    assert result["severity"] == CheckSeverity.FAIL
    assert result["data"]["raw_log_path"] is None
    assert result["data"]["raw_output_summary"]
    assert any(
        "failed to write local raw log" in warning
        for warning in result["data"]["warnings"]
    )
