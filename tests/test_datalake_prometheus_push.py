"""Tests for datalake.prometheus.push_gateway (Phase 08-04)."""
from __future__ import annotations

from unittest.mock import patch

import pytest
from workspace_core.config import ServerSpec

from datalake.prometheus.push_gateway import (
    RESOURCE_METRIC_NAMES,
    PushError,
    build_latest_telemetry_exposition,
    build_telemetry_exposition,
    push_metrics,
    push_telemetry_metrics,
)


class _FakeTunnel:
    def __init__(self) -> None:
        self.stopped = False

    def stop(self, timeout_s: float = 3.0) -> None:
        self.stopped = True


def _spec() -> ServerSpec:
    return ServerSpec(
        name="A2-AK-225",
        host="192.168.9.225",
        user="root",
        conda_env="verl-qwen3.5",
        workdir="/home/t00906153",
    )


def test_push_metrics_posts_text_exposition():
    spec = _spec()
    tunnel = _FakeTunnel()
    with patch("datalake.prometheus.push_gateway.open_reverse_tunnel", return_value=tunnel) as tunnel_mock, \
         patch("datalake.prometheus.push_gateway.run_in_env", return_value=(0, "", "")) as mock:
        assert push_metrics(spec, "run 123/abc", 8, pushgateway_url="http://host:9091")

    command = mock.call_args.args[1]
    assert "autoresearch_npu_count" in command
    assert 'run_id="run_123_abc"' in command
    assert "http://host:9091/metrics/job/ar_run_123_abc" in command
    assert mock.call_args.kwargs["conda_env"] == "verl-qwen3.5"
    assert mock.call_args.kwargs["workdir"] == "/home/t00906153"
    assert tunnel.stopped is True
    assert tunnel_mock.called


def test_build_telemetry_exposition_includes_resource_metrics_and_labels():
    exposition = build_telemetry_exposition(
        [
            {
                "run_id": "run 123",
                "case_id": "sync-1024-2048",
                "server": "A2-AK-225",
                "device_id": 0,
                "source": "npu-smi-watch",
                "hbm_used_mib": 1234,
                "hbm_total_mib": 65536,
                "ai_core_utilization_percent": 71,
                "npu_utilization_percent": 44,
            }
        ]
    )

    for metric_name in RESOURCE_METRIC_NAMES:
        assert metric_name in exposition
    assert 'run_id="run 123"' in exposition
    assert 'case_id="sync-1024-2048"' in exposition
    assert 'server="A2-AK-225"' in exposition
    assert 'device_id="0"' in exposition
    assert 'source="npu-smi-watch"' in exposition


def test_build_telemetry_exposition_returns_empty_without_samples():
    assert build_telemetry_exposition([]) == ""


def test_latest_telemetry_exposition_collapses_duplicate_label_sets():
    exposition = build_latest_telemetry_exposition(
        [
            {
                "run_id": "run123",
                "case_id": "sync-1024-2048",
                "server": "A2-AK-225",
                "device_id": 0,
                "sample_index": 1,
                "hbm_used_mib": 1000,
            },
            {
                "run_id": "run123",
                "case_id": "sync-1024-2048",
                "server": "A2-AK-225",
                "device_id": 0,
                "sample_index": 2,
                "hbm_used_mib": 1234,
            },
        ]
    )

    assert exposition.count("autoresearch_npu_hbm_used_mib{") == 1
    assert "1234" in exposition
    assert "sample_index" not in exposition


def test_push_telemetry_metrics_posts_resource_text_exposition():
    spec = _spec()
    tunnel = _FakeTunnel()
    samples = [
        {
            "run_id": "run123",
            "case_id": "sync-1024-2048",
            "server": "A2-AK-225",
            "device_id": 0,
            "source": "npu-smi-watch",
            "hbm_used_mib": 1234,
        }
    ]
    with patch("datalake.prometheus.push_gateway.open_reverse_tunnel", return_value=tunnel), \
         patch("datalake.prometheus.push_gateway.run_in_env", return_value=(0, "", "")) as mock:
        assert push_telemetry_metrics(spec, "run123", samples, pushgateway_url="http://host:9091")

    command = mock.call_args.args[1]
    assert "autoresearch_npu_hbm_used_mib" in command
    assert 'case_id="sync-1024-2048"' in command
    assert "http://host:9091/metrics/job/ar_run123" in command
    assert tunnel.stopped is True


def test_push_metrics_raises_on_negative_count():
    with pytest.raises(PushError, match="不能为负数"):
        push_metrics(_spec(), "run123", -1)


def test_push_metrics_raises_on_curl_failure():
    tunnel = _FakeTunnel()
    with patch("datalake.prometheus.push_gateway.open_reverse_tunnel", return_value=tunnel), \
         patch(
             "datalake.prometheus.push_gateway.run_in_env",
             return_value=(7, "", "Connection refused"),
         ):
        with pytest.raises(PushError, match="pushgateway 推送失败"):
            push_metrics(_spec(), "run123", 8)
    assert tunnel.stopped is True
