"""Tests for verl-workspace-adapter minimal runners (Phase 08-01, D-44)."""
from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest
from workspace_core.config import ServerSpec
from workspace_core.ssh import CommandTimeoutError

from verl_workspace_adapter.common import conda_utils as _conda
from verl_workspace_adapter.common.conda_utils import run_in_env, build_conda_command, build_cd_command
from verl_workspace_adapter.verl.minimal_runner import (
    run_minimal,
    _parse_one_step_output,
    ONE_STEP_SCRIPT_TMPL,
    MinimalResult,
)
from verl_workspace_adapter.veomni.minimal_runner import run_minimal as run_minimal_veomni


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


# === _parse_one_step_output ===

def test_parse_one_step_pass():
    stdout = "[INFO] some startup\nSUM= 5.29\nNPU_COUNT= 8\n"
    s, n = _parse_one_step_output(stdout)
    assert s == 5.29
    assert n == 8


def test_parse_one_step_missing_sum():
    stdout = "NPU_COUNT= 8\n"
    s, n = _parse_one_step_output(stdout)
    assert s is None
    assert n == 8


def test_parse_one_step_empty():
    s, n = _parse_one_step_output("")
    assert s is None
    assert n is None


# === run_minimal PASS / fail / timeout ===

def _mock_spec():
    return ServerSpec(name="test", host="1.2.3.4", user="root")


def test_run_minimal_pass():
    spec = _mock_spec()
    with patch("verl_workspace_adapter.verl.minimal_runner.run_in_env") as mock:
        mock.return_value = (0, "[INFO] init\nSUM= 5.29\nNPU_COUNT= 8\n", "")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root", lib="verl")
    assert r["lib"] == "verl"
    assert r["sum_value"] == 5.29
    assert r["npu_count"] == 8
    assert r["exit_code"] == 0
    assert r["timeout"] is False
    assert r["error"] is None
    # 命令应该含 conda run + cd
    # runner 传给 run_in_env 的原始 command (含 torch_npu)
    # cd + conda run 是 run_in_env 内部拼的, 这里看不到
    called_cmd = mock.call_args[0][1]
    assert "torch_npu" in called_cmd
    assert "torch_npu, verl" in called_cmd  # lib 默认 verl (与 torch_npu 并列 import)


def test_run_minimal_veomni_lib():
    spec = _mock_spec()
    with patch("verl_workspace_adapter.veomni.minimal_runner.run_in_env") as mock:
        mock.return_value = (0, "SUM= 7.58\nNPU_COUNT= 8\n", "")
        r = run_minimal_veomni(spec, conda_env="veomni_qwen35", workdir="/root")
    assert r["lib"] == "veomni"
    assert r["sum_value"] == 7.58
    assert r["npu_count"] == 8
    assert r["exit_code"] == 0
    called_cmd = mock.call_args[0][1]
    assert "torch_npu, veomni" in called_cmd  # lib 占位被替换


def test_run_minimal_timeout():
    spec = _mock_spec()
    with patch("verl_workspace_adapter.verl.minimal_runner.run_in_env") as mock:
        mock.side_effect = CommandTimeoutError("test timeout 30s")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root")
    assert r["timeout"] is True
    assert r["exit_code"] == -1
    assert "timeout" in r["error"]


def test_run_minimal_exit_nonzero():
    spec = _mock_spec()
    with patch("verl_workspace_adapter.verl.minimal_runner.run_in_env") as mock:
        mock.return_value = (1, "", "ModuleNotFoundError: No module named 'verl'")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root")
    assert r["exit_code"] == 1
    assert r["sum_value"] is None
    assert "ModuleNotFoundError" in r["stderr"]


def test_run_minimal_no_sum_in_stdout():
    spec = _mock_spec()
    with patch("verl_workspace_adapter.verl.minimal_runner.run_in_env") as mock:
        mock.return_value = (0, "wandb init...\nNPU_COUNT= 8\n", "")
        r = run_minimal(spec, conda_env="verl-qwen3.5", workdir="/root")
    assert r["sum_value"] is None
    assert r["npu_count"] == 8
    assert r["exit_code"] == 0
