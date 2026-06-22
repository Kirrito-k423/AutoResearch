"""Tests for formal Verl NPU telemetry helpers."""
from __future__ import annotations

import importlib

import pytest


telemetry = importlib.import_module("workspace-adapter.verl.telemetry")


def test_npu_smi_watch_command_uses_native_one_second_sampling():
    command = telemetry.build_npu_smi_watch_command()

    assert "command -v npu-smi" in command
    assert "/usr/local/Ascend/driver/tools/npu-smi" in command
    assert '"$NPU_SMI_BIN" info watch -d 1 -s amn' in command


def test_npu_smi_watch_command_rejects_half_second_sampling():
    with pytest.raises(ValueError, match="integer seconds"):
        telemetry.build_npu_smi_watch_command(0.5)


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
    assert summary.sample_interval_seconds == 1
    assert summary.max_hbm_used_mib == 900
    assert summary.hbm_total_mib == 1000
    assert summary.max_ai_core_utilization_percent == 90
    assert summary.max_npu_utilization_percent == 80
