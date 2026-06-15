"""Tests for autoresearch.stack.checker (Phase 07-01 + 07-02)."""
import json
import pytest
from unittest.mock import patch, MagicMock

from autoresearch.stack import checker as _checker
from autoresearch.stack.checker import (
    check_stack,
    run_stack_check,
    check_library,
    probe_conda_env,
    run_one_step_dryrun,
    check_all_servers,
    ONE_STEP_SCRIPT_TMPL,
    DIAG_ENV_MISSING_TMPL,
)


# === Constants / structure (D-41 NPU adaptation) ===

def test_one_step_script_uses_torch_npu_not_cuda():
    """1-step 干跑脚本必须用 torch_npu (NPU 适配 — 用户明确要求, D-41)."""
    assert "torch_npu" in ONE_STEP_SCRIPT_TMPL
    assert ".npu()" in ONE_STEP_SCRIPT_TMPL
    assert ".cuda()" not in ONE_STEP_SCRIPT_TMPL
    assert "verl.trainer" not in ONE_STEP_SCRIPT_TMPL


def test_diag_env_missing_template_includes_env_name():
    """D-42.D1: env 缺失诊断含 env 名."""
    msg = DIAG_ENV_MISSING_TMPL.format(env="verl-env")
    assert "verl-env" in msg
    assert "conda env create" in msg


# === Server resolution ===

def test_check_stack_config_error_returns_fail(tmp_path):
    """未知 server -> fail, error 含 ConfigError 消息."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "only", "host": "10.0.0.1", "user": "root"}],
    }))
    result = check_stack("ghost", config_path=cfg_path)
    assert result["ok"] is False
    assert "配置错误" in (result["error"] or "")
    assert "ghost" in (result["error"] or "")


# === Conda env probe (D-40) ===

def test_probe_conda_env_when_no_env_configured():
    """config.conda_env 空 -> 提示走系统 python."""
    spec = MagicMock()
    spec.conda_env = ""
    result = probe_conda_env(spec)
    assert result["exists"] is False
    assert "未配" in (result["detail"] or "")


def test_probe_conda_env_exists():
    """`conda env list` 含 env 名 -> exists=True."""
    spec = MagicMock()
    spec.conda_env = "verl-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (0, "# conda environments:\n#\nverl-env   /opt/conda/envs/verl-env\nbase      /opt/conda\n", "")
        result = probe_conda_env(spec)
    assert result["exists"] is True
    assert result["name"] == "verl-env"


def test_probe_conda_env_missing_with_diag():
    """env 不在 -> exists=False, detail 含 D-42.D1 诊断."""
    spec = MagicMock()
    spec.conda_env = "ghost-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (0, "# conda environments:\nbase   /opt/conda\n", "")
        result = probe_conda_env(spec)
    assert result["exists"] is False
    assert "ghost-env" in (result["detail"] or "")
    assert "conda env create" in (result["detail"] or "")


# === Library check (D-39) ===

def test_check_library_pass_returns_version():
    """`import <lib>; print(<lib>.__version__)` exit 0 + 输出 -> version 解析."""
    spec = MagicMock()
    spec.conda_env = "verl-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (0, "0.2.0\n", "")
        chk = check_library(spec, "verl")
    assert chk["ok"] is True
    assert chk["version"] == "0.2.0"


def test_check_library_import_error_diag():
    """import 失败 -> ok=False, detail 含 D-42.D2 诊断 (env 名 + lib 名)."""
    spec = MagicMock()
    spec.conda_env = "verl-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (1, "", "ModuleNotFoundError: No module named 'verl'")
        chk = check_library(spec, "verl")
    assert chk["ok"] is False
    assert "verl-env" in (chk["detail"] or "")
    assert "verl" in (chk["detail"] or "")
    assert "pip install" in (chk["detail"] or "")


# === 1-step dryrun (D-41 NPU adaptation) ===

def test_one_step_pass_parses_sum_and_npu_count():
    """1-step exit 0 + stdout SUM + NPU_COUNT -> ok=True, npu_device_count 透出."""
    spec = MagicMock()
    spec.name = "A2-AK-225"
    spec.conda_env = "verl-env"
    stdout = "SUM= 6.0\nNPU_COUNT= 8\n"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (0, stdout, "")
        result = run_one_step_dryrun(spec, "verl")
    assert result["ok"] is True
    assert result["sum_value"] == 6.0
    assert result["npu_device_count"] == 8


def test_one_step_timeout_returns_warning():
    """1-step 30s timeout -> ok=False, warning 含 D-42.D3 诊断 (含 server 名)."""
    from workspace_core.ssh.exceptions import CommandTimeoutError
    spec = MagicMock()
    spec.name = "A2-AK-225"
    spec.conda_env = "verl-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.side_effect = CommandTimeoutError("timeout")
        result = run_one_step_dryrun(spec, "verl", timeout=30.0)
    assert result["ok"] is False
    assert result["warning"] is not None
    assert "NPU 通信" in result["warning"]
    assert "A2-AK-225" in result["warning"]


def test_one_step_exit_nonzero_returns_warning():
    """1-step exit != 0 -> ok=False, warning 含 D-42 诊断."""
    spec = MagicMock()
    spec.name = "A2-AK-225"
    spec.conda_env = "verl-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (1, "", "ImportError: No module named 'torch_npu'")
        result = run_one_step_dryrun(spec, "verl")
    assert result["ok"] is False
    assert result["warning"] is not None
    assert "verl" in result["warning"]


def test_one_step_no_sum_in_stdout_returns_warning():
    """1-step stdout 无 SUM= -> ok=False, warning 含 D-42 诊断."""
    spec = MagicMock()
    spec.name = "A2-AK-225"
    spec.conda_env = "verl-env"
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.return_value = (0, "weird output\n", "")
        result = run_one_step_dryrun(spec, "verl")
    assert result["ok"] is False
    assert "SUM=" in (result["warning"] or "")


# === Top-level aggregation ===

def test_check_stack_happy_path():
    """env 存在 + libs ok + 1-step ok -> overall ok=True, severity=ok."""
    import yaml
    cfg_path = tmp_path_fixture()
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.side_effect = lambda *a, **kw: _mock_uat(args=a, kwargs=kw, mode="happy")
        result = check_stack("srv", config_path=cfg_path, libs=("verl",))
    assert result["ok"] is True
    assert result["severity"] == "ok"
    assert result["conda_env"]["exists"] is True
    assert result["libraries"]["verl"]["ok"] is True
    assert result["one_step"] is not None
    assert result["one_step"]["ok"] is True


def test_check_stack_env_missing_fails():
    """env 不存在 -> fail."""
    # 改 cfg 配 ghost-env, 然后 mock 返 env_missing
    import yaml
    from pathlib import Path
    import tempfile
    cfg_path = Path(tempfile.mkdtemp()) / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "srv", "host": "1.2.3.4", "user": "root", "conda_env": "ghost-env"}],
    }))
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.side_effect = lambda *a, **kw: _mock_uat(args=a, kwargs=kw, mode="env_missing")
        result = check_stack("srv", config_path=cfg_path, libs=("verl",))
    assert result["ok"] is False
    assert result["severity"] == "fail"
    assert "ghost-env" in (result["error"] or "")


def test_check_stack_one_step_timeout_warns():
    """env ok + libs ok + 1-step timeout -> ok=True, severity=warn (D-41.C6)."""
    cfg_path = tmp_path_fixture()
    with patch.object(_checker, "_ssh_exec_capture") as m:
        m.side_effect = lambda *a, **kw: _mock_uat(args=a, kwargs=kw, mode="one_step_timeout")
        result = check_stack("srv", config_path=cfg_path, libs=("verl",))
    assert result["ok"] is True  # warn 算 pass
    assert result["severity"] == "warn"
    assert result["one_step"]["ok"] is False


# === CLI boundary ===

def test_run_stack_check_writes_json(capsys, tmp_path):
    """run_stack_check 单一 JSON stdout + exit 0/1."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "ok-srv", "host": "1.2.3.4", "user": "root", "conda_env": "verl-env"}],
    }))
    with patch.object(_checker, "check_stack") as m:
        m.return_value = {
            "server": "ok-srv", "ok": True, "severity": "ok",
            "conda_env": {"name": "verl-env", "exists": True, "python_version": None, "detail": None},
            "libraries": {"verl": {"library": "verl", "version": "0.2.0", "ok": True, "detail": None, "warning": None}},
            "one_step": {"ok": True, "npu_device_count": 8, "sum_value": 6.0, "elapsed_ms": 100, "detail": None, "warning": None},
            "error": None,
        }
        rc = run_stack_check("ok-srv", config=cfg_path)
    assert rc == 0
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["data"]["server"] == "ok-srv"


# === Fixtures / helpers ===

def tmp_path_fixture():
    import yaml
    import tempfile
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp()) / "cfg.yaml"
    tmp.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "srv", "host": "1.2.3.4", "user": "root", "conda_env": "verl-env"}],
    }))
    return tmp


def _mock_uat(args, kwargs, mode):
    """根据 mode 返 mock SSH 响应."""
    cmd = args[1] if len(args) > 1 else ""
    if "conda env list" in cmd:
        if mode == "env_missing":
            return (0, "base   /opt/conda\n", "")
        return (0, "verl-env   /opt/conda/envs/verl-env\nbase   /opt/conda\n", "")
    if "import verl" in cmd:
        return (0, "0.2.0\n", "")
    if "torch.randn" in cmd:
        if mode == "one_step_timeout":
            from workspace_core.ssh.exceptions import CommandTimeoutError
            raise CommandTimeoutError("30s timeout")
        return (0, "SUM= 6.0\nNPU_COUNT= 8\n", "")
    return (0, "", "")


# === --all (D-07/D-29) ===

def test_check_all_servers_passes_when_all_ok(tmp_path):
    """4 台全 OK -> overall ok=True, passed=4."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [
            {"name": "s1", "host": "1.1.1.1", "user": "root"},
            {"name": "s2", "host": "2.2.2.2", "user": "root"},
            {"name": "s3", "host": "3.3.3.3", "user": "root"},
            {"name": "s4", "host": "4.4.4.4", "user": "root"},
        ],
    }))
    fake = lambda n, *a, **kw: {
        "server": n, "ok": True, "severity": "ok",
        "conda_env": {"name": "", "exists": False, "python_version": None, "detail": "no env"},
        "libraries": {}, "one_step": None, "error": None,
    }
    with patch.object(_checker, "check_stack", side_effect=fake):
        summary = check_all_servers(config_path=cfg_path)
    assert summary["total"] == 4
    assert summary["passed"] == 4
    assert summary["failed"] == 0


def test_check_all_servers_isolates_one_failure(tmp_path):
    """1 台 fail 隔离, 3 台 OK -> overall fail, failed=1."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [
            {"name": "good-1", "host": "1.1.1.1", "user": "root"},
            {"name": "bad-1", "host": "2.2.2.2", "user": "root"},
            {"name": "good-2", "host": "3.3.3.3", "user": "root"},
        ],
    }))
    def fake(n, *a, **kw):
        if n == "bad-1":
            return {
                "server": n, "ok": False, "severity": "fail",
                "conda_env": {"name": "x", "exists": False, "python_version": None, "detail": "no env"},
                "libraries": {"verl": {"library": "verl", "version": None, "ok": False, "detail": "fail", "warning": None}},
                "one_step": None, "error": "boom",
            }
        return {
            "server": n, "ok": True, "severity": "ok",
            "conda_env": {"name": "", "exists": False, "python_version": None, "detail": ""},
            "libraries": {}, "one_step": None, "error": None,
        }
    with patch.object(_checker, "check_stack", side_effect=fake):
        summary = check_all_servers(config_path=cfg_path)
    assert summary["passed"] == 2
    assert summary["failed"] == 1
    assert summary["failed_servers"] == ["bad-1"]


def test_check_all_servers_preserves_config_order(tmp_path):
    """结果按 config 顺序排, 不按 worker 完成时间."""
    import yaml, time
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [
            {"name": "slow-1", "host": "1.1.1.1", "user": "root"},
            {"name": "fast-1", "host": "2.2.2.2", "user": "root"},
            {"name": "fast-2", "host": "3.3.3.3", "user": "root"},
        ],
    }))
    def fake(n, *a, **kw):
        time.sleep(0.1 if n.startswith("slow") else 0.01)
        return {
            "server": n, "ok": True, "severity": "ok",
            "conda_env": {"name": "", "exists": False, "python_version": None, "detail": ""},
            "libraries": {}, "one_step": None, "error": None,
        }
    with patch.object(_checker, "check_stack", side_effect=fake):
        summary = check_all_servers(config_path=cfg_path)
    assert list(summary["results"].keys()) == ["slow-1", "fast-1", "fast-2"]


# 改 import 把 check_all_servers 加进来
