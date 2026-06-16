"""Tests for workspace-adapter minimal runners (Phase 08-01, D-44)."""
from __future__ import annotations

from unittest.mock import patch, MagicMock
import importlib

import pytest
from workspace_core.config import ServerSpec
from workspace_core.ssh import CommandTimeoutError

_conda = importlib.import_module("workspace-adapter.common.conda_utils")
_verl_runner = importlib.import_module("workspace-adapter.verl.minimal_runner")
_veomni_runner = importlib.import_module("workspace-adapter.veomni.minimal_runner")

run_in_env = _conda.run_in_env
build_conda_command = _conda.build_conda_command
build_cd_command = _conda.build_cd_command
run_minimal = _verl_runner.run_minimal
_parse_one_step_output = _verl_runner._parse_one_step_output
ONE_STEP_SCRIPT_TMPL = _verl_runner.ONE_STEP_SCRIPT_TMPL
MinimalResult = _verl_runner.MinimalResult
run_minimal_veomni = _veomni_runner.run_minimal


# === conda_utils ===

def test_build_conda_command_with_env():
    assert build_conda_command("verl-qwen3.5", "python -c x") == "conda run -n verl-qwen3.5 python -c x"


def test_build_conda_command_empty_env():
    """D-40: 空 env 走系统 python, 不加 conda run."""
    assert build_conda_command("", "python -c x") == "python -c x"


def test_build_cd_command_with_workdir():
    assert build_cd_command("/root", "ls") == "cd '/root' && ls"


def test_build_cd_command_empty():
    """D-46: 空 workdir 直通."""
    assert build_cd_command("", "ls") == "ls"


def test_build_cd_command_escapes_single_quote():
    """D-46: 路径含单引号不破."""
    assert build_cd_command("/root/it's", "ls") == "cd '/root/it'\\''s' && ls"


def test_run_in_env_wraps_cd_before_conda():
    """D-46: cd 必须在 conda run 外层, 否则 conda 会尝试执行 cd 二进制."""
    spec = _mock_spec()
    with patch.object(_conda, "_ssh_exec_capture", return_value=(0, "", "")) as mock:
        run_in_env(spec, "python x.py", conda_env="verl-env", workdir="/root")
    assert mock.call_args.args[1] == "cd '/root' && conda run -n verl-env python x.py"


# === _parse_one_step_output ===

def test_parse_one_step_pass():
    stdout = "[INFO] some startup\nSUM= 5.29\nNPU_COUNT= 8\n"
    s, n, w = _parse_one_step_output(stdout)
    assert s == 5.29
    assert n == 8


def test_parse_one_step_missing_sum():
    stdout = "NPU_COUNT= 8\n"
    s, n, w = _parse_one_step_output(stdout)
    assert s is None
    assert n == 8


def test_parse_one_step_empty():
    s, n, w = _parse_one_step_output("")
    assert s is None
    assert n is None


# === run_minimal PASS / fail / timeout ===

def _mock_spec():
    return ServerSpec(name="test", host="1.2.3.4", user="root")


from contextlib import contextmanager

@contextmanager
def _patch_runner_io(remote_return):
    """统一 patch runner 用的 SSHClient.sftp + run_in_env (D-45 1-step)."""
    with patch.object(_verl_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient, \
         patch("workspace_core.secrets.resolve_secret", return_value=None):
        MockClient.return_value.sftp.return_value = MagicMock()
        if remote_return is not None:
            mock_run.return_value = remote_return
        yield mock_run


def test_run_minimal_pass():
    spec = _mock_spec()
    with patch.object(_verl_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient:
        MockClient.return_value.sftp.return_value = MagicMock()  # sftp.put mock
        mock_run.return_value = (0, "[INFO] init\nSUM= 5.29\nNPU_COUNT= 8\n", "")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root", lib="verl")
    assert r["lib"] == "verl"
    assert r["sum_value"] == 5.29
    assert r["npu_count"] == 8
    assert r["exit_code"] == 0
    assert r["timeout"] is False
    assert r["error"] is None
    # runner 传给 run_in_env 的原始 command (含 torch_npu, lib)
    # D-45: runner 写本地脚本 + SFTP 上传, 调 run_in_env 跑的 command 是
    # `mkdir -p <wandb_dir> && WANDB_DIR=... python /tmp/one_step_*.py`
    called_cmd = mock_run.call_args[0][1]
    assert "/tmp/one_step_" in called_cmd
    assert "WANDB_DIR=/root/wandb" in called_cmd


def test_run_minimal_with_run_id_tees_remote_log():
    spec = _mock_spec()
    with patch.object(_verl_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient:
        MockClient.return_value.sftp.return_value = MagicMock()
        mock_run.return_value = (0, "SUM= 5.29\nNPU_COUNT= 8\n", "")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root", run_id="run123")
    called_cmd = mock_run.call_args.args[1]
    assert "tee -a /root/runs/run123.log" in called_cmd
    assert r["remote_log_path"] == "/root/runs/run123.log"


def test_run_minimal_veomni_lib():
    spec = _mock_spec()
    with patch.object(_veomni_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient:
        MockClient.return_value.sftp.return_value = MagicMock()
        mock_run.return_value = (0, "SUM= 7.58\nNPU_COUNT= 8\n", "")
        r = run_minimal_veomni(spec, conda_env="veomni_qwen35", workdir="/root")
    assert r["lib"] == "veomni"
    assert r["sum_value"] == 7.58
    assert r["npu_count"] == 8
    assert r["exit_code"] == 0
    called_cmd = mock_run.call_args[0][1]
    assert "/tmp/one_step_" in called_cmd
    assert "WANDB_DIR=/root/wandb" in called_cmd


def test_run_minimal_timeout():
    spec = _mock_spec()
    with patch.object(_verl_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient:
        MockClient.return_value.sftp.return_value = MagicMock()
        mock_run.side_effect = CommandTimeoutError("test timeout 30s")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root")
    assert r["timeout"] is True
    assert r["exit_code"] == -1
    assert "timeout" in r["error"]


def test_run_minimal_exit_nonzero():
    spec = _mock_spec()
    with patch.object(_verl_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient:
        MockClient.return_value.sftp.return_value = MagicMock()
        mock_run.return_value = (1, "", "ModuleNotFoundError: No module named 'verl'")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root")
    assert r["exit_code"] == 1
    assert r["sum_value"] is None
    assert "ModuleNotFoundError" in r["stderr"]


def test_run_minimal_no_sum_in_stdout():
    spec = _mock_spec()
    with patch.object(_verl_runner, "run_in_env") as mock_run, \
         patch("workspace_core.ssh.client.SSHClient") as MockClient:
        MockClient.return_value.sftp.return_value = MagicMock()
        mock_run.return_value = (0, "wandb init...\nNPU_COUNT= 8\n", "")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root")
    assert r["sum_value"] is None
    assert r["npu_count"] == 8
    assert r["exit_code"] == 0
