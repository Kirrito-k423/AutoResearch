"""Tests for autoresearch.collect.minimal (Phase 08-01, D-44)."""
from __future__ import annotations

import json
import pytest
from unittest.mock import patch, MagicMock

from workspace_core.config import ConfigError, ServerSpec
from autoresearch.collect.minimal import (
    collect_minimal,
    _resolve_workdir,
    _resolve_spec,
    _LIB_TO_RUNNER,
)


def _spec_dict(name="A2-AK-225", conda_env="verl-qwen3.5", workdir="/root"):
    return {
        "name": name,
        "host": "192.168.9.225",
        "port": 22,
        "user": "root",
        "conda_env": conda_env,
        # D-46 workdir 字段 08-03 才加, 08-01 getattr 兜底
    }


# === _resolve_workdir (D-46 兜底) ===

def test_resolve_workdir_override():
    """D-46: override 优先."""
    s = ServerSpec(name="t", host="1.2.3.4", user="root")
    assert _resolve_workdir(s, "/tmp/override") == "/tmp/override"


def test_resolve_workdir_default():
    """D-46: 没 override + 没字段 → 兜底 /root."""
    s = ServerSpec(name="t", host="1.2.3.4", user="root")
    assert _resolve_workdir(s, None) == "/root"


def test_resolve_workdir_empty_override_falls_back_to_default():
    """D-46: override 是空字符串 → 兜底 /root."""
    s = ServerSpec(name="t", host="1.2.3.4", user="root")
    assert _resolve_workdir(s, "") == "/root"


def test_resolve_workdir_uses_spec_field():
    """D-46: ServerSpec.workdir 正式落地."""
    s = ServerSpec(name="t", host="1.2.3.4", user="root", workdir="/home/t00906153")
    assert _resolve_workdir(s, None) == "/home/t00906153"


# === _resolve_spec ===

def test_resolve_spec_found(tmp_path):
    config = tmp_path / "c.yaml"
    config.write_text("""\
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.9.225
    user: root
    conda_env: verl-qwen3.5
""")
    s = _resolve_spec("A2-AK-225", config)
    assert s.name == "A2-AK-225"
    assert s.conda_env == "verl-qwen3.5"


def test_resolve_spec_not_found(tmp_path):
    config = tmp_path / "c.yaml"
    config.write_text("""\
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.9.225
    user: root
""")
    with pytest.raises(ConfigError, match="找不到 server=missing"):
        _resolve_spec("missing", config)


# === collect_minimal 派发 ===

def test_collect_minimal_dispatches_verl(tmp_path):
    config = tmp_path / "c.yaml"
    config.write_text("""\
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.9.225
    user: root
    conda_env: verl-qwen3.5
""")
    with patch("workspace-adapter.verl.minimal_runner.run_minimal") as mock:
        mock.return_value = {"lib": "verl", "sum_value": 5.29, "npu_count": 8, "exit_code": 0, "elapsed_ms": 22000, "stdout": "SUM= 5.29", "stderr": "", "error": None, "timeout": False}
        r = collect_minimal("A2-AK-225", lib="verl", config_path=config, run_id="run123")
    assert r["sum_value"] == 5.29
    assert r["npu_count"] == 8
    # runner 接到正确参数
    kwargs = mock.call_args.kwargs
    assert kwargs["lib"] == "verl"
    assert kwargs["conda_env"] == "verl-qwen3.5"
    assert kwargs["workdir"] == "/root"  # 兜底
    assert kwargs["run_id"] == "run123"


def test_collect_minimal_dispatches_veomni(tmp_path):
    config = tmp_path / "c.yaml"
    config.write_text("""\
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.9.225
    user: root
    conda_env: veomni_qwen35
""")
    with patch("workspace-adapter.veomni.minimal_runner.run_minimal") as mock:
        mock.return_value = {"lib": "veomni", "sum_value": 7.58, "npu_count": 8, "exit_code": 0, "elapsed_ms": 19000, "stdout": "SUM= 7.58", "stderr": "", "error": None, "timeout": False}
        r = collect_minimal("A2-AK-225", lib="veomni", config_path=config)
    assert r["sum_value"] == 7.58
    kwargs = mock.call_args.kwargs
    assert kwargs["lib"] == "veomni"
    assert kwargs["conda_env"] == "veomni_qwen35"


def test_collect_minimal_unsupported_lib_raises(tmp_path):
    config = tmp_path / "c.yaml"
    config.write_text("version: 1\nservers:\n  - name: X\n    host: 1.1.1.1\n    user: root\n")
    with pytest.raises(ValueError, match="不支持"):
        collect_minimal("X", lib="torchtune", config_path=config)


def test_collect_minimal_lib_dispatch_map():
    """D-43 决策: 仅 verl/veomni, 派发表锁定 2 入口."""
    assert set(_LIB_TO_RUNNER.keys()) == {"verl", "veomni"}
    assert _LIB_TO_RUNNER["verl"] == "workspace-adapter.verl.minimal_runner"
    assert _LIB_TO_RUNNER["veomni"] == "workspace-adapter.veomni.minimal_runner"
