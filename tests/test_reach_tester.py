"""Tests for autoresearch.reach.tester — single server reach (Phase 06-02)."""
import json
import pytest
from unittest.mock import patch, MagicMock

from autoresearch.reach import tester as _tester
from autoresearch.reach.tester import (
    run_reach_test,
    _build_wandb_curl,
    _build_pushgateway_curl,
    WANDB_HEALTH_URL,
    PUSHGATEWAY_REMOTE_PORT,
    WANDB_REMOTE_PORT,
    WANDB_LOCAL_URL,
)


# === Constants / structure ===

def test_constants_align_with_decisions():
    """D-35: wandb 走 17890; D-38: pushgateway 走 17891."""
    assert WANDB_HEALTH_URL == "http://127.0.0.1:17890/healthz"
    assert WANDB_REMOTE_PORT == 17890
    assert PUSHGATEWAY_REMOTE_PORT == 17891


def test_build_wandb_curl_hits_17890_healthz():
    cmd = _build_wandb_curl()
    assert "127.0.0.1:17890/healthz" in cmd
    assert "curl" in cmd
    assert "-X GET" in cmd or "GET" not in cmd  # curl 默认 GET, 不强制写


def test_ensure_wandb_tunnel_targets_local_wandb_port():
    """wandb reach 隧道必须转到本机 8080, 不能复用默认代理 7890."""
    from autoresearch.reach.tester import _ensure_wandb_tunnel, _heartbeat_wandb_tunnel

    with patch("autoresearch.net.tunnel.ensure_tunnel") as ensure:
        ensure.return_value = {"remote_port": WANDB_REMOTE_PORT, "pid": 123}
        assert _ensure_wandb_tunnel("A2-AK-225", "config/config.yaml") == (
            8080,
            WANDB_REMOTE_PORT,
            123,
        )
    ensure.assert_called_once()
    kwargs = ensure.call_args.kwargs
    assert kwargs["local_proxy_url"] == WANDB_LOCAL_URL
    assert kwargs["remote_proxy_port"] == WANDB_REMOTE_PORT
    assert kwargs["heartbeat_fn"] is _heartbeat_wandb_tunnel


def test_build_pushgateway_curl_has_metric_body():
    cmd = _build_pushgateway_curl("A2-AK-225")
    assert "127.0.0.1:17891/metrics/job/autoresearch_reach/instance/A2-AK-225" in cmd
    assert "autoresearch_reach_test" in cmd
    assert 'server="A2-AK-225"' in cmd
    assert "1" in cmd  # gauge value


# === Server resolution ===

def test_resolve_server_missing_raises_config_error(tmp_path):
    """未知 server -> ConfigError, 包装成 fail result."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "only-one", "host": "10.0.0.1", "user": "root"}],
    }))
    result = _tester.test_server_reach("does-not-exist", config_path=cfg_path)
    assert result["ok"] is False
    assert "配置错误" in (result["error"] or "")
    assert "does-not-exist" in (result["error"] or "")


# === Wandb check (D-35.A4) ===

def test_check_wandb_pass_with_state_available():
    """wandb /healthz 返 state==available -> ok=True."""
    from autoresearch.reach.tester import _check_wandb
    spec = MagicMock()
    spec.user = "root"
    spec.host = "1.2.3.4"
    spec.port = 22
    spec.identity_file = "/tmp/k"
    spec.bootstrap_password_secret = None
    with patch("autoresearch.reach.tester._ssh_exec_capture") as m:
        m.return_value = (0, json.dumps({"state": "available"}), "")
        chk = _check_wandb(spec)
    assert chk["ok"] is True
    assert chk["status_code"] == 200
    assert chk["latency_ms"] is not None


def test_check_wandb_pass_with_ready_text():
    """新版 wandb/local /healthz 返回 ready! 文本也应视为健康."""
    from autoresearch.reach.tester import _check_wandb

    spec = MagicMock()
    spec.user = "root"
    spec.host = "1.2.3.4"
    spec.port = 22
    spec.identity_file = "/tmp/k"
    spec.bootstrap_password_secret = None
    with patch("autoresearch.reach.tester._ssh_exec_capture") as m:
        m.return_value = (0, "ready!", "")
        chk = _check_wandb(spec)
    assert chk["ok"] is True
    assert chk["status_code"] == 200


def test_check_wandb_fail_when_state_wrong():
    """wandb /healthz 返 state!=available -> ok=False, detail 包含 state 值."""
    from autoresearch.reach.tester import _check_wandb
    spec = MagicMock()
    spec.user = "root"
    spec.host = "1.2.3.4"
    spec.port = 22
    spec.identity_file = "/tmp/k"
    spec.bootstrap_password_secret = None
    with patch("autoresearch.reach.tester._ssh_exec_capture") as m:
        m.return_value = (0, json.dumps({"state": "down"}), "")
        chk = _check_wandb(spec)
    assert chk["ok"] is False
    assert "down" in (chk["detail"] or "")


def test_check_wandb_fail_on_non_json_body():
    """wandb /healthz 返非 ready 文本 -> ok=False."""
    from autoresearch.reach.tester import _check_wandb
    spec = MagicMock()
    spec.user = "root"
    spec.host = "1.2.3.4"
    spec.port = 22
    spec.identity_file = "/tmp/k"
    spec.bootstrap_password_secret = None
    with patch("autoresearch.reach.tester._ssh_exec_capture") as m:
        m.return_value = (0, "OK\n", "")  # plain text
        chk = _check_wandb(spec)
    assert chk["ok"] is False
    assert "不表示 ready" in (chk["detail"] or "")


# === Pushgateway check (D-38.D4 best-effort) ===

def test_check_pushgateway_pass_on_2xx():
    """pushgateway push 成功 -> ok=True."""
    from autoresearch.reach.tester import _check_pushgateway
    spec = MagicMock()
    spec.user = "root"
    spec.host = "1.2.3.4"
    spec.port = 22
    spec.identity_file = "/tmp/k"
    spec.bootstrap_password_secret = None
    spec.name = "test-srv"
    with patch("autoresearch.reach.tester._ssh_exec_capture") as m:
        m.return_value = (0, "", "")
        chk = _check_pushgateway(spec, push_tunnel=None)
    assert chk["ok"] is True
    assert chk["warning"] is None


def test_check_pushgateway_fail_returns_warning_not_error():
    """push 失败 -> ok=False, 有 warning (best-effort, D-38.D4)."""
    from autoresearch.reach.tester import _check_pushgateway
    spec = MagicMock()
    spec.user = "root"
    spec.host = "1.2.3.4"
    spec.port = 22
    spec.identity_file = "/tmp/k"
    spec.bootstrap_password_secret = None
    spec.name = "test-srv"
    with patch("autoresearch.reach.tester._ssh_exec_capture") as m:
        m.return_value = (56, "", "Recv failure: Connection reset by peer")
        chk = _check_pushgateway(spec, push_tunnel=None)
    assert chk["ok"] is False
    assert chk["warning"] is not None
    assert "best-effort" in chk["warning"]


# === CLI boundary ===

def test_run_reach_test_writes_json(capsys, tmp_path):
    """run_reach_test 单一 JSON stdout + 走 progress 协议."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "ok-srv", "host": "1.2.3.4", "user": "root", "identity_file": "/tmp/k"}],
    }))
    fake_wandb = {
        "name": "wandb", "ok": True, "latency_ms": 5,
        "status_code": 200, "detail": None, "warning": None,
    }
    fake_push = {
        "name": "pushgateway", "ok": True, "latency_ms": 6,
        "status_code": 200, "detail": None, "warning": None,
    }
    with patch("autoresearch.reach.tester._ensure_wandb_tunnel") as tw, \
         patch("autoresearch.reach.tester._open_pushgateway_tunnel") as tp, \
         patch("autoresearch.reach.tester._check_wandb", return_value=fake_wandb), \
         patch("autoresearch.reach.tester._check_pushgateway", return_value=fake_push):
        tw.return_value = (8080, 17890, 100)
        tp.return_value = MagicMock(pid=200)
        rc = run_reach_test("ok-srv", config=cfg_path)
    assert rc == 0
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["data"]["server"] == "ok-srv"


def test_run_reach_test_wandb_fail_returns_nonzero(capsys, tmp_path):
    """wandb 失败 -> exit 1, error 含 DIAG_HINT."""
    import yaml
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": [{"name": "bad-srv", "host": "1.2.3.4", "user": "root", "identity_file": "/tmp/k"}],
    }))
    fake_wandb = {
        "name": "wandb", "ok": False, "latency_ms": 7230,
        "status_code": None, "detail": "curl exit=22", "warning": None,
    }
    fake_push = {
        "name": "pushgateway", "ok": False, "latency_ms": 7854,
        "status_code": None, "detail": "ssh fail",
        "warning": "pushgateway push 异常 (best-effort, 不阻塞主流程)",
    }
    with patch("autoresearch.reach.tester._ensure_wandb_tunnel") as tw, \
         patch("autoresearch.reach.tester._open_pushgateway_tunnel") as tp, \
         patch("autoresearch.reach.tester._check_wandb", return_value=fake_wandb), \
         patch("autoresearch.reach.tester._check_pushgateway", return_value=fake_push):
        tw.return_value = (8080, 17890, 100)
        tp.return_value = MagicMock(pid=200)
        rc = run_reach_test("bad-srv", config=cfg_path)
    assert rc == 1
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert payload["ok"] is False
    assert payload["error"]
    assert "请先跑" in payload["error"]
    assert "net tunnel ensure" in payload["error"]


# === --all (D-07/D-29) ===

def test_all_servers_passes_when_all_ok(tmp_path):
    """4 台全 OK -> overall ok=True, passed=4, failed=0."""
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
    fake_result = lambda name: {
        "server": name, "ok": True, "severity": "ok",
        "wandb": {"name": "wandb", "ok": True, "latency_ms": 5, "status_code": 200, "detail": None, "warning": None},
        "pushgateway": {"name": "pushgateway", "ok": True, "latency_ms": 6, "status_code": 200, "detail": None, "warning": None},
        "host": "x", "tunnel_wandb": "pid=1", "tunnel_pushgateway": "pid=2", "error": None,
    }
    with patch("autoresearch.reach.tester.test_server_reach", side_effect=lambda n, *a, **kw: fake_result(n)):
        from autoresearch.reach.tester import test_all_servers
        summary = test_all_servers(config_path=cfg_path)
    assert summary["total"] == 4
    assert summary["passed"] == 4
    assert summary["failed"] == 0
    assert summary["failed_servers"] == []
    assert summary["passed_servers"] == ["s1", "s2", "s3", "s4"]


def test_all_servers_isolates_one_failure(tmp_path):
    """1 台 fail 隔离, 3 台仍 ok -> overall fail, passed=3, failed=1."""
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
                "wandb": {"name": "wandb", "ok": False, "latency_ms": None, "status_code": None, "detail": "x", "warning": None},
                "pushgateway": {"name": "pushgateway", "ok": False, "latency_ms": None, "status_code": None, "detail": "y", "warning": None},
                "host": "x", "tunnel_wandb": None, "tunnel_pushgateway": None, "error": "boom",
            }
        return {
            "server": n, "ok": True, "severity": "ok",
            "wandb": {"name": "wandb", "ok": True, "latency_ms": 5, "status_code": 200, "detail": None, "warning": None},
            "pushgateway": {"name": "pushgateway", "ok": True, "latency_ms": 6, "status_code": 200, "detail": None, "warning": None},
            "host": "x", "tunnel_wandb": "p", "tunnel_pushgateway": "p", "error": None,
        }
    with patch("autoresearch.reach.tester.test_server_reach", side_effect=fake):
        from autoresearch.reach.tester import test_all_servers
        summary = test_all_servers(config_path=cfg_path)
    assert summary["total"] == 3
    assert summary["passed"] == 2
    assert summary["failed"] == 1
    assert summary["failed_servers"] == ["bad-1"]


def test_all_servers_preserves_config_order(tmp_path):
    """结果按 config 顺序排, 不按 worker 完成顺序."""
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
            "wandb": {"name": "wandb", "ok": True, "latency_ms": 1, "status_code": 200, "detail": None, "warning": None},
            "pushgateway": {"name": "pushgateway", "ok": True, "latency_ms": 1, "status_code": 200, "detail": None, "warning": None},
            "host": "x", "tunnel_wandb": "p", "tunnel_pushgateway": "p", "error": None,
        }
    with patch("autoresearch.reach.tester.test_server_reach", side_effect=fake):
        from autoresearch.reach.tester import test_all_servers
        summary = test_all_servers(config_path=cfg_path)
    assert list(summary["results"].keys()) == ["slow-1", "fast-1", "fast-2"]
