"""Tests for the pure Ascend npu-smi parser."""
from pathlib import Path

from autoresearch.hw.parser import (
    parse_driver_version_info,
    parse_lspci_devices,
    parse_npu_smi_info,
    parse_processes,
    parse_ps_output,
    parse_typed_metric_output,
)


FIXTURES = Path(__file__).parent / "fixtures" / "hw"


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_baseline_parses_eight_ascend_devices_with_core_metrics():
    result = parse_npu_smi_info(
        _fixture("npu_smi_25_3_rc1_no_processes.txt")
    )

    assert result["error"] is None
    assert result["field_errors"] == []
    assert result["driver_versions"]["npu_smi"] == "25.3.rc1"
    assert len(result["devices"]) == 8
    assert {device["name"] for device in result["devices"]} == {"Ascend 910B2"}
    assert {device["memory_total_mib"] for device in result["devices"]} == {65536}
    for device in result["devices"]:
        assert isinstance(device["memory_used_mib"], int)
        assert isinstance(device["memory_total_mib"], int)
        assert isinstance(device["temperature_c"], int)
        assert isinstance(device["utilization_pct"], int)


def test_no_process_marker_produces_empty_process_list():
    result = parse_npu_smi_info(
        _fixture("npu_smi_25_3_rc1_no_processes.txt")
    )

    assert result["processes"] == []


def test_process_fixture_parses_only_strict_numeric_records():
    text = _fixture("npu_smi_with_processes.txt")
    warnings: list[str] = []

    processes = parse_processes(text, warnings)

    assert processes == [
        {
            "npu_id": 0,
            "chip_id": 0,
            "pid": 4102,
            "user": None,
            "process_name": None,
            "memory_used_mib": 2048,
        }
    ]
    assert len(warnings) == 2
    assert "87;touch" not in repr(processes)


def test_ps_parser_uses_only_pid_user_and_executable_name():
    details = parse_ps_output(
        " 4102 trainer /usr/bin/python3\n"
        "bad root /bin/sh\n"
        "4103 missing-field\n"
    )

    assert details == {4102: ("trainer", "/usr/bin/python3")}


def test_missing_and_invalid_metrics_are_null_with_field_errors():
    result = parse_npu_smi_info(_fixture("npu_smi_missing_metric.txt"))

    assert result["error"] is None
    assert len(result["devices"]) == 1
    device = result["devices"][0]
    assert device["name"] == "Ascend 910B2"
    assert device["health"] == "OK"
    assert device["bus_id"] == "0000:81:00.0"
    assert device["memory_used_mib"] == 3467
    assert device["memory_total_mib"] is None
    assert device["temperature_c"] is None
    assert device["utilization_pct"] is None
    assert {error["field"] for error in result["field_errors"]} == {
        "memory_total_mib",
        "temperature_c",
        "utilization_pct",
    }


def test_missing_device_table_returns_parse_failure_without_raising():
    result = parse_npu_smi_info(_fixture("npu_smi_unknown_format.txt"))

    assert result["devices"] == []
    assert result["error"] is not None


def test_variant_headers_parse_without_fixed_column_widths():
    result = parse_npu_smi_info(_fixture("npu_smi_variant.txt"))

    assert result["error"] is None
    assert result["field_errors"] == []
    assert [device["name"] for device in result["devices"]] == [
        "Ascend 910B",
        "Ascend 910 Premium",
    ]
    assert result["devices"][0]["memory_total_mib"] == 32768
    assert result["devices"][1]["temperature_c"] == 39
    assert result["devices"][1]["utilization_pct"] == 5


def test_typed_metric_parser_returns_only_recognized_values():
    memory = parse_typed_metric_output(
        "| NPU ID | Memory Usage (MiB) |\n| 3 | 1234 / 65536 |\n",
        "memory",
        3,
    )
    temp = parse_typed_metric_output(
        "| Device ID | Temperature (C) |\n| 3 | 42 C |\n",
        "temp",
        3,
    )
    usages = parse_typed_metric_output(
        "| ID | AI Core Utilization (%) |\n| 3 | 71% |\n",
        "usages",
        3,
    )

    assert memory == {
        "memory_used_mib": 1234,
        "memory_total_mib": 65536,
    }
    assert temp == {"temperature_c": 42}
    assert usages == {"utilization_pct": 71}
    assert parse_typed_metric_output("unsupported", "temp", 3) == {}


def test_driver_version_info_parses_driver_and_package_versions():
    versions = parse_driver_version_info(_fixture("driver_version_info.txt"))

    assert versions == {
        "npu_smi": None,
        "driver": "25.3.rc1",
        "package": "25.3.rc1",
    }


def test_lspci_parser_keeps_only_huawei_ascend_processing_accelerators():
    devices = parse_lspci_devices(_fixture("lspci_ascend.txt"))

    assert [device["bus_id"] for device in devices] == [
        "0000:31:00.0",
        "0000:32:00.0",
    ]
    assert all(
        "Processing accelerators" in device["description"]
        for device in devices
    )
    assert all(
        device[field] is None
        for device in devices
        for field in (
            "memory_total_mib",
            "memory_used_mib",
            "temperature_c",
            "utilization_pct",
        )
    )
