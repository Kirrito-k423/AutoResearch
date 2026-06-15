"""Tests for `autoresearch collect run` (Phase 08-04)."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.collect.cli import run_collect
from datalake.logs import LogFetchError


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(
        """\
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.9.225
    user: root
    conda_env: verl-qwen3.5
    workdir: /home/t00906153
""",
        encoding="utf-8",
    )
    return path


def test_run_collect_happy_path_writes_manifest(tmp_path):
    cfg = _config(tmp_path)
    local_root = tmp_path / "runs"
    minimal = {
        "lib": "verl",
        "sum_value": 5.29,
        "npu_count": 8,
        "elapsed_ms": 1234,
        "exit_code": 0,
        "stdout": "SUM= 5.29\nNPU_COUNT= 8\n",
        "stderr": "",
        "error": None,
        "timeout": False,
        "wandb_run_id": "abc123",
        "remote_log_path": "/home/t00906153/runs/run123.log",
    }

    with patch("autoresearch.collect.cli.collect_minimal", return_value=minimal) as mock_minimal, \
         patch("autoresearch.collect.cli.sync_run", return_value=local_root / "run123" / "wandb") as mock_sync, \
         patch("autoresearch.collect.cli.collect_log", return_value=local_root / "run123" / "log.txt") as mock_log, \
         patch("autoresearch.collect.cli.push_metrics", return_value=True) as mock_push:
        exit_code, payload = run_collect(
            server="A2-AK-225",
            lib="verl",
            config=str(cfg),
            workdir=None,
            timeout=30.0,
            run_id="run123",
            local_runs_root=local_root,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["prom_pushed"] is True
    assert Path(payload["manifest"]).exists()
    data = json.loads(Path(payload["manifest"]).read_text())
    assert data["run_id"] == "run123"
    assert data["workdir_remote"] == "/home/t00906153"
    assert data["one_step"]["npu_count"] == 8
    assert mock_minimal.call_args.kwargs["run_id"] == "run123"
    assert mock_minimal.call_args.kwargs["workdir_override"] == "/home/t00906153"
    assert mock_sync.call_args.kwargs["workdir"] == "/home/t00906153"
    assert mock_log.call_args.kwargs["remote_log_path"] == "/home/t00906153/runs/run123.log"
    assert mock_push.call_args.args[2] == 8


def test_run_collect_keeps_manifest_when_downstream_steps_fail(tmp_path):
    cfg = _config(tmp_path)
    local_root = tmp_path / "runs"
    minimal = {
        "lib": "verl",
        "sum_value": None,
        "npu_count": None,
        "elapsed_ms": 0,
        "exit_code": 1,
        "stdout": "",
        "stderr": "boom",
        "error": "boom",
        "timeout": False,
        "wandb_run_id": None,
        "remote_log_path": "/home/t00906153/runs/run123.log",
    }

    with patch("autoresearch.collect.cli.collect_minimal", return_value=minimal), \
         patch("autoresearch.collect.cli.collect_log", side_effect=LogFetchError("raw log error")):
        exit_code, payload = run_collect(
            server="A2-AK-225",
            lib="verl",
            config=str(cfg),
            workdir=None,
            timeout=30.0,
            run_id="run123",
            local_runs_root=local_root,
        )

    assert exit_code == 1
    assert payload["ok"] is False
    assert Path(payload["manifest"]).exists()
    data = json.loads(Path(payload["manifest"]).read_text())
    assert data["exit_code"] == 1
    assert "minimal run failed" in data["error"]
    assert "raw log error" in payload["errors"][1]


def test_collect_run_cli_outputs_single_json_object(tmp_path):
    runner = CliRunner()
    with patch(
        "autoresearch.collect.cli.run_collect",
        return_value=(0, {"ok": True, "run_id": "run123"}),
    ) as mock:
        result = runner.invoke(main, ["collect", "run", "--server", "A2-AK-225"])

    assert result.exit_code == 0
    assert json.loads(result.output) == {"ok": True, "run_id": "run123"}
    assert mock.call_args.kwargs["server"] == "A2-AK-225"
