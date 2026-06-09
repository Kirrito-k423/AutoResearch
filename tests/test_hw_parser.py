"""Tests for the pure Ascend npu-smi parser."""
from pathlib import Path

from autoresearch.hw.parser import parse_npu_smi_info


FIXTURES = Path(__file__).parent / "fixtures" / "hw"


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_baseline_parses_eight_ascend_devices_with_core_metrics():
    result = parse_npu_smi_info(
        _fixture("npu_smi_25_3_rc1_no_processes.txt")
    )

    assert result["error"] is None
    assert result["field_errors"] == []
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
    result = parse_npu_smi_info("| unsupported | output |\n")

    assert result["devices"] == []
    assert result["error"] is not None
