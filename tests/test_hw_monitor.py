"""Tests for long-running hardware telemetry monitor."""
from __future__ import annotations

import json

from workspace_core.config import ServerSpec

from autoresearch.hw.monitor import NPU_SMI_ONCE_COMMAND, run_monitor


def _server() -> ServerSpec:
    return ServerSpec(
        name="A2-AK-225",
        host="192.0.2.225",
        user="root",
        conda_env="verl-qwen3.5",
        workdir="/home/t00906153",
    )


def test_hw_monitor_once_pushes_machine_metrics(monkeypatch, tmp_path, capsys):
    config = tmp_path / "config.yaml"
    config.write_text(
        """
version: 1
servers:
  - name: A2-AK-225
    host: 192.0.2.225
    port: 22
    user: root
network:
  enabled: false
  targets: []
log:
  level: INFO
  json: false
  dir: ~/.autoresearch/logs
wandb:
  enabled: true
  project: autoresearch
""",
        encoding="utf-8",
    )
    commands = []
    pushed = []

    def fake_runner(spec, command, timeout):
        commands.append((spec.name, command, timeout))
        return (
            0,
            """
2026-06-23 10:00:00
| NPU   Name                | Health        | Power(W)    Temp(C)           Hugepages-Usage(page)|
| Chip                      | Bus-Id        | AICore(%)   Memory-Usage(MB)  HBM-Usage(MB)        |
| 0     910B2               | OK            | 108.8       39                0    / 0             |
| 0                         | 0000:C1:00.0  | 7           0    / 0          49290/ 65536         |
""",
            "",
        )

    def fake_push(endpoint, body):
        pushed.append((endpoint, body))
        return True

    exit_code = run_monitor(
        server="A2-AK-225",
        config=config,
        once=True,
        runner=fake_runner,
        push_text=fake_push,
    )

    stdout = capsys.readouterr().out
    payload = json.loads(stdout)
    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["data"]["samples"] == 1
    assert payload["data"]["pushes"] == 1
    assert commands[0][0] == "A2-AK-225"
    assert NPU_SMI_ONCE_COMMAND in commands[0][1]
    assert pushed[0][0].endswith("/metrics/job/autoresearch_machine/server/A2-AK-225")
    assert "autoresearch_machine_npu_hbm_used_mib" in pushed[0][1]
    assert "autoresearch_machine_npu_sample_time_seconds" in pushed[0][1]
    assert 'server="A2-AK-225"' in pushed[0][1]
    assert 'device_id="0"' in pushed[0][1]
    assert 'chip_id="0"' in pushed[0][1]


def test_hw_monitor_rejects_sub_half_second_interval(capsys):
    exit_code = run_monitor(
        server="A2-AK-225",
        interval_seconds=0.1,
        once=True,
        runner=lambda *_args, **_kwargs: (0, "", ""),
        push_text=lambda *_args, **_kwargs: True,
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["ok"] is False
    assert "interval" in payload["error"]
