"""Tests for datalake.prometheus.push_gateway (Phase 08-04)."""
from __future__ import annotations

from unittest.mock import patch

import pytest
from workspace_core.config import ServerSpec

from datalake.prometheus.push_gateway import PushError, push_metrics


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
