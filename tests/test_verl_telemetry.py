"""Tests for formal Verl NPU telemetry helpers."""
from __future__ import annotations

import importlib

import pytest


telemetry = importlib.import_module("workspace-adapter.verl.telemetry")


def test_npu_smi_watch_command_uses_half_second_sampling():
    command = telemetry.build_npu_smi_watch_command()

    assert "command -v npu-smi" in command
    assert "/usr/local/sbin/npu-smi" in command
    assert '"$NPU_SMI_BIN" info' in command
    assert "sleep 0.5" in command


def test_npu_smi_watch_command_can_include_host_resource_sampling():
    command = telemetry.build_npu_smi_watch_command(include_host_metrics=True)

    assert "__AR_HOST_MEMORY__" in command
    assert "__AR_HOST_CPU__" in command
    assert "/proc/meminfo" in command
    assert "/proc/stat /proc/stat" in command


def test_npu_smi_watch_command_rejects_too_fast_sampling():
    with pytest.raises(ValueError, match=r"\[0.5, 100\]"):
        telemetry.build_npu_smi_watch_command(0.25)


def test_parse_watch_table_preserves_correlation_labels():
    text = """
2026-06-22 14:50:01
| NPU ID | AI Core Usage(%) | Memory Usage(MiB) | NPU Utilization(%) |
| 0      | 71               | 1234 / 65536      | 44                 |
| 1      | 5                | 2048 / 65536      | 8                  |
"""

    samples = telemetry.parse_npu_smi_watch_output(
        text,
        run_id="run-a",
        case_id="case-1",
        server="A2-AK-225",
    )

    assert len(samples) == 2
    first = samples[0]
    assert first.run_id == "run-a"
    assert first.case_id == "case-1"
    assert first.server == "A2-AK-225"
    assert first.device_id == 0
    assert first.source == "npu-smi-watch"
    assert first.observed_at == "2026-06-22 14:50:01"
    assert first.hbm_used_mib == 1234
    assert first.hbm_total_mib == 65536
    assert first.ai_core_utilization_percent == 71
    assert first.npu_utilization_percent == 44


def test_parse_npu_smi_info_table_extracts_hbm_and_aicore():
    text = """
2026-06-22 21:20:01
| NPU   Name                | Health        | Power(W)    Temp(C)           Hugepages-Usage(page)|
| Chip                      | Bus-Id        | AICore(%)   Memory-Usage(MB)  HBM-Usage(MB)        |
| 0     910B2               | OK            | 108.8       39                0    / 0             |
| 0                         | 0000:C1:00.0  | 7           0    / 0          49290/ 65536         |
"""

    samples = telemetry.parse_npu_smi_watch_output(
        text,
        run_id="run-a",
        case_id="case-1",
        server="A2-AK-225",
    )

    assert len(samples) == 1
    assert samples[0].device_id == 0
    assert samples[0].hbm_used_mib == 49290
    assert samples[0].hbm_total_mib == 65536
    assert samples[0].ai_core_utilization_percent == 7


def test_parse_dual_chip_info_table_preserves_chip_identity():
    text = """
2026-06-22 21:20:01
| NPU   Name                | Health        | Power(W)    Temp(C)           Hugepages-Usage(page)|
| Chip  Phy-ID              | Bus-Id        | AICore(%)   Memory-Usage(MB)  HBM-Usage(MB)        |
| 0     Ascend910           | OK            | 165.4       44                0    / 0             |
| 0     0                   | 0000:9D:00.0  | 0           0    / 0          29726/ 65536         |
| 0     Ascend910           | OK            | -           41                0    / 0             |
| 1     1                   | 0000:9F:00.0  | 0           0    / 0          29498/ 65536         |
| 1     Ascend910           | OK            | 166.1       42                0    / 0             |
| 0     2                   | 0000:99:00.0  | 0           0    / 0          3088 / 65536         |
| 1     Ascend910           | OK            | -           43                0    / 0             |
| 1     3                   | 0000:9B:00.0  | 0           0    / 0          2882 / 65536         |
"""

    samples = telemetry.parse_npu_smi_watch_output(
        text,
        run_id="run-a",
        case_id="case-1",
        server="A3-AX-180",
    )
    summary = telemetry.summarize_telemetry(samples)

    assert len(samples) == 4
    assert [sample.device_id for sample in samples] == [0, 0, 1, 1]
    assert [sample.chip_id for sample in samples] == [0, 1, 2, 3]
    assert summary.device_count == 4


def test_parse_watch_output_can_label_host_side_source():
    samples = telemetry.parse_npu_smi_watch_output(
        """
| NPU | AI Core | HBM Usage(MB) | NPU Utilization |
| 0   | 10      | 100 / 1000    | 20              |
""",
        run_id="run-a",
        case_id="case-1",
        server="A2-AK-225",
        source=telemetry.SOURCE_HOST_NPU_SMI_WATCH,
    )

    assert samples[0].source == "host-npu-smi-watch"


def test_parse_host_metrics_output_extracts_cpu_and_memory():
    samples = telemetry.parse_host_metrics_output(
        """
2026-06-22 21:20:01
__AR_HOST_SAMPLE__ sample_time_seconds=1782153601.25
__AR_HOST_MEMORY__ used_bytes=34359738368 total_bytes=68719476736 free_bytes=17179869184 available_bytes=51539607552 shared_bytes=1073741824 buff_cache_bytes=17179869184 occupied_bytes=51539607552 utilization_percent=50.000000 occupied_percent=75.000000
__AR_HOST_CPU__ utilization_percent=37.500000
""",
        run_id="run-a",
        case_id="case-1",
        server="A3-AX-180",
    )

    assert len(samples) == 1
    assert samples[0].server == "A3-AX-180"
    assert samples[0].source == "host-resource-watch"
    assert samples[0].observed_at == "2026-06-22 21:20:01"
    assert samples[0].sample_time_seconds == 1782153601.25
    assert samples[0].memory_used_bytes == 34359738368
    assert samples[0].memory_total_bytes == 68719476736
    assert samples[0].memory_free_bytes == 17179869184
    assert samples[0].memory_available_bytes == 51539607552
    assert samples[0].memory_shared_bytes == 1073741824
    assert samples[0].memory_buff_cache_bytes == 17179869184
    assert samples[0].memory_occupied_bytes == 51539607552
    assert samples[0].memory_utilization_percent == 50
    assert samples[0].memory_occupied_percent == 75
    assert samples[0].cpu_utilization_percent == 37.5


def test_summarize_telemetry_tracks_peak_values():
    samples = telemetry.parse_npu_smi_watch_output(
        """
| NPU | AI Core | HBM Usage(MB) | NPU Utilization |
| 0   | 10      | 100 / 1000    | 20              |
| 0   | 90      | 900 / 1000    | 80              |
""",
        run_id="run-a",
        case_id="case-1",
        server="A2-AK-225",
    )

    summary = telemetry.summarize_telemetry(samples)

    assert summary.sample_count == 2
    assert summary.device_count == 1
    assert summary.sample_interval_seconds == 0.5
    assert summary.max_hbm_used_mib == 900
    assert summary.hbm_total_mib == 1000
    assert summary.max_ai_core_utilization_percent == 90
    assert summary.max_npu_utilization_percent == 80
