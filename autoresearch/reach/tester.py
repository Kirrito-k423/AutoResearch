"""autoresearch.reach.tester — reach test 单机实现 (D-35..D-38).

核心入口 `test_server_reach(server_name, ...)`:
  1. _ensure_tunnel_for_reach: 通过 net.tunnel.ensure_tunnel 建直连 17890 -> 本机 wandb:8080
     + 17891 -> 本机 pushgateway:9091 (pushgateway 不写 state)
  2. 远程 ssh curl http://127.0.0.1:17890/healthz 验 wandb
  3. 远程 ssh curl -X PUT http://127.0.0.1:17891/metrics/job/... 推 pushgateway metric
  4. 汇总 wandb + pushgateway -> ReachResult

不引第三方客户端 (D-36 决策): 用裸 curl + workspace_core.ssh.SSHClient.
不写新 dep.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from workspace_core.config import ServerSpec, from_path, ConfigError
from workspace_core.progress import emit_progress
from workspace_core.ssh import (
    AuthError,
    BootstrapFailed,
    HostSpec,
    SSHClient,
    SSHError,
    TunnelError,
)
from workspace_core.ssh.tunnel import ReverseTunnel, open_reverse_tunnel

from .models import ReachCheck, ReachResult, ReachSummary

# === Constants (D-35, D-36, D-38) ===

WANDB_REMOTE_PORT = 17890   # 远端直连本机 wandb:8080
WANDB_HEALTH_PATH = "/healthz"
WANDB_HEALTH_URL = f"http://127.0.0.1:{WANDB_REMOTE_PORT}{WANDB_HEALTH_PATH}"
WANDB_HEALTH_EXPECTED_BODY_KEY = "state"  # {"state": "available"} -> PASS
WANDB_HEALTH_EXPECTED_VALUE = "available"
WANDB_READY_TEXT = "ready!"

PUSHGATEWAY_REMOTE_PORT = 17891   # Phase 6 引入 (不写 state, reach 期间临时)
PUSHGATEWAY_PUSH_PATH_TMPL = (
    "/metrics/job/autoresearch_reach/instance/{server}"
)
PUSHGATEWAY_LOCAL_PORT = 9091     # 本机 pushgateway 容器端口 (D-36.B1)

WANDB_LOCAL_PORT = 8080           # 本机 wandb 容器端口
WANDB_LOCAL_URL = f"http://127.0.0.1:{WANDB_LOCAL_PORT}"

# Metric body template (D-38.D2)
PUSHGATEWAY_METRIC_TMPL = """# HELP autoresearch_reach_test Reach test pass/fail gauge
# TYPE autoresearch_reach_test gauge
autoresearch_reach_test{{server="{server}"}} {value}
# HELP autoresearch_reach_timestamp_seconds Last reach probe unix ts
# TYPE autoresearch_reach_timestamp_seconds gauge
autoresearch_reach_timestamp_seconds{{server="{server}"}} {ts}
"""

DIAG_HINT = (
    "请先跑 `autoresearch net tunnel ensure --server {alias}`"
)


# === Server resolution ===

def _resolve_server(server_name: str, config_path: str | Path | None) -> ServerSpec:
    cfg = from_path(str(config_path) if config_path else None)
    spec = next((s for s in cfg.servers if s.name == server_name), None)
    if spec is None:
        avail = [s.name for s in cfg.servers]
        raise ConfigError(
            f"config.servers 中找不到 '{server_name}'; 已配: {avail}"
        )
    return spec


def _host_spec(spec: ServerSpec) -> HostSpec:
    # SSHClient 不展开 ~, 这里手动展开 (Phase 4 同样问题)
    id_file = None
    if spec.identity_file:
        id_file = str(Path(spec.identity_file).expanduser())
    return HostSpec(
        alias=spec.name,
        host=spec.host,
        port=spec.port,
        user=spec.user,
        identity_file=id_file,
    )


# === Tunnel management ===

def _ensure_wandb_tunnel(
    server_name: str,
    config_path: str | Path | None,
) -> tuple[int, int, int | None]:
    """确保 wandb tunnel (17890) 就绪.

    Returns: (local_port, remote_port, pid)
    Raises:  TunnelError / ConfigError
    """
    from autoresearch.net.tunnel import ensure_tunnel  # lazy import
    state = ensure_tunnel(
        server_name,
        config_path=config_path,
        local_proxy_url=WANDB_LOCAL_URL,
        remote_proxy_port=WANDB_REMOTE_PORT,
        heartbeat_fn=_heartbeat_wandb_tunnel,
    )
    return (
        WANDB_LOCAL_PORT,
        state["remote_port"],
        int(state["pid"]),
    )


def _heartbeat_wandb_tunnel(
    server_name: str,
    state: dict[str, Any],
    config_path: str | Path | None = None,
) -> bool:
    """Heartbeat for a direct wandb reverse tunnel, not an HTTP proxy tunnel."""
    from autoresearch.net.tunnel import is_process_alive

    if not is_process_alive(state["pid"]):
        return False
    try:
        spec = _resolve_server(server_name, config_path)
        ec, so, _ = _ssh_exec_capture(spec, _build_wandb_curl(), timeout=10.0)
        return ec == 0 and _wandb_health_body_ok(so.strip())
    except Exception:
        return False


def _open_pushgateway_tunnel(
    host: HostSpec,
    local_port: int = PUSHGATEWAY_LOCAL_PORT,
) -> ReverseTunnel:
    """为 pushgateway 临时起一条 ssh -R 17891:localhost:9091.

    **不写 state** (D-36 决策: 避免覆盖 wandb 17890 state). reach 期间使用,
    退出 reach 时由 _close_pushgateway_tunnel 关掉.
    """
    return open_reverse_tunnel(
        host,
        remote_port=PUSHGATEWAY_REMOTE_PORT,
        local_port=local_port,
        identity_file=Path(host.identity_file) if host.identity_file else None,
    )


def _close_pushgateway_tunnel(tunnel: ReverseTunnel | None) -> None:
    """Reach 完后关 pushgateway 临时 tunnel."""
    if tunnel is None:
        return
    try:
        tunnel.stop(timeout_s=3.0)
    except Exception:
        pass


# === Remote curl commands ===

def _build_remote_curl(url: str, method: str = "GET", body: str | None = None) -> str:
    """构造远程 curl 命令 (无 ALL_PROXY, 我们走 127.0.0.1 直接命中 tunnel).

    timeout 8s, fail-on-error, silent 输出.
    """
    parts = ["curl", "-fsS", "-m", "8", "-X", method, url]
    if body is not None:
        # 用 heredoc 避免 shell 注入 (body 不含 $ 即可)
        parts.extend(["--data-binary", "@-"])
        return " ".join(parts) + " <<'AR_BODY_EOF'\n" + body + "\nAR_BODY_EOF"
    return " ".join(parts)


def _build_wandb_curl() -> str:
    return _build_remote_curl(WANDB_HEALTH_URL, method="GET")


def _build_pushgateway_curl(server: str) -> str:
    url = f"http://127.0.0.1:{PUSHGATEWAY_REMOTE_PORT}" + PUSHGATEWAY_PUSH_PATH_TMPL.format(server=server)
    body = PUSHGATEWAY_METRIC_TMPL.format(
        server=server,
        value=1,    # 默认 1=PASS, 失败时改 0
        ts=int(time.time()),
    )
    return _build_remote_curl(url, method="PUT", body=body)


# === Per-server SSH helpers ===

def _ssh_exec_capture(
    spec: ServerSpec,
    command: str,
    timeout: float = 12.0,
) -> tuple[int, str, str]:
    """用 workspace_core SSHClient 跑命令, 返 (exit_code, stdout, stderr)."""
    from workspace_core.secrets import resolve_secret
    pw = resolve_secret(spec.bootstrap_password_secret) if spec.bootstrap_password_secret else None
    client = SSHClient(
        _host_spec(spec),
        bootstrap_password=pw,
    )
    try:
        client.connect(connect_timeout=5.0)
    except (AuthError, SSHError) as e:
        raise BootstrapFailed(f"SSH 连接失败: {e}") from e
    try:
        ec, so, se = client.exec(command, timeout=timeout)
        return ec, so, se
    finally:
        client.close()


# === Reach checks ===

def _check_wandb(spec: ServerSpec) -> ReachCheck:
    """远程 curl wandb /healthz, 验 body 含 state==available."""
    t0 = time.perf_counter()
    try:
        ec, so, se = _ssh_exec_capture(spec, _build_wandb_curl(), timeout=10.0)
        latency = int((time.perf_counter() - t0) * 1000)
        body = so.strip()
        if ec != 0:
            return ReachCheck(
                name="wandb",
                ok=False,
                latency_ms=latency,
                status_code=None,
                detail=f"curl exit={ec}: {se.strip()[:200]}",
                warning=None,
            )
        if _wandb_health_body_ok(body):
            return ReachCheck(
                name="wandb", ok=True, latency_ms=latency,
                status_code=200, detail=None, warning=None,
            )
        return ReachCheck(
            name="wandb", ok=False, latency_ms=latency,
            status_code=200, detail=f"body 不表示 ready: {body[:100]}",
            warning=None,
        )
    except Exception as e:
        latency = int((time.perf_counter() - t0) * 1000)
        return ReachCheck(
            name="wandb", ok=False, latency_ms=latency,
            status_code=None, detail=str(e)[:200], warning=None,
        )


def _wandb_health_body_ok(body: str) -> bool:
    """Accept both old JSON health and current wandb/local text health."""
    text = body.strip()
    if text == WANDB_READY_TEXT:
        return True
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    return data.get(WANDB_HEALTH_EXPECTED_BODY_KEY) == WANDB_HEALTH_EXPECTED_VALUE


def _check_pushgateway(
    spec: ServerSpec,
    push_tunnel: ReverseTunnel | None,
) -> ReachCheck:
    """远程 push metric 到 pushgateway; 失败 best-effort warn (D-38.D4)."""
    t0 = time.perf_counter()
    try:
        # 等 pushgateway tunnel 就绪 (open_reverse_tunnel 后给 0.5s 让 ssh -R 起来)
        if push_tunnel is not None:
            time.sleep(0.5)
        ec, so, se = _ssh_exec_capture(spec, _build_pushgateway_curl(spec.name), timeout=10.0)
        latency = int((time.perf_counter() - t0) * 1000)
        if ec == 0:
            return ReachCheck(
                name="pushgateway", ok=True, latency_ms=latency,
                status_code=200, detail=None, warning=None,
            )
        # push 失败 -> warn (best-effort, D-38.D4)
        return ReachCheck(
            name="pushgateway", ok=False, latency_ms=latency,
            status_code=None, detail=f"curl exit={ec}: {se.strip()[:200]}",
            warning="pushgateway push 失败 (best-effort, 不阻塞主流程)",
        )
    except Exception as e:
        latency = int((time.perf_counter() - t0) * 1000)
        return ReachCheck(
            name="pushgateway", ok=False, latency_ms=latency,
            status_code=None, detail=str(e)[:200],
            warning="pushgateway push 异常 (best-effort, 不阻塞主流程)",
        )


# === Top-level entry ===

def test_server_reach(
    server_name: str,
    config_path: str | Path | None = None,
    lang: str = "zh",
) -> ReachResult:
    """单台 reach test 入口.

    步骤:
      1. 调 _ensure_wandb_tunnel 建/验 17890 隧道 (复用 Phase 5 state)
      2. 调 _open_pushgateway_tunnel 临时起 17891 (不写 state)
      3. 远程 _check_wandb
      4. 远程 _check_pushgateway
      5. 汇总 -> ReachResult
      6. _close_pushgateway_tunnel 收尾

    失败诊断 (D-37): 探测失败 -> 错误信息含 DIAG_HINT.
    """
    emit_progress("reach.test.start", server=server_name)
    push_tunnel: ReverseTunnel | None = None
    try:
        spec = _resolve_server(server_name, config_path)
    except ConfigError as e:
        return ReachResult(
            server=server_name, ok=False, severity="fail",
            wandb=ReachCheck(name="wandb", ok=False, latency_ms=None,
                             status_code=None, detail=None, warning=None),
            pushgateway=ReachCheck(name="pushgateway", ok=False, latency_ms=None,
                                   status_code=None, detail=None, warning=None),
            host="", tunnel_wandb=None, tunnel_pushgateway=None,
            error=f"配置错误: {e}",
        )

    # 1. 建 wandb tunnel (17890 -> 本机 8080)
    tunnel_wandb_pid: int | None = None
    try:
        _, _, tunnel_wandb_pid = _ensure_wandb_tunnel(server_name, config_path)
    except (TunnelError, ConfigError) as e:
        hint = DIAG_HINT.format(alias=server_name)
        return ReachResult(
            server=server_name, ok=False, severity="fail",
            wandb=ReachCheck(name="wandb", ok=False, latency_ms=None,
                             status_code=None, detail=None, warning=None),
            pushgateway=ReachCheck(name="pushgateway", ok=False, latency_ms=None,
                                   status_code=None, detail=None, warning=None),
            host=spec.host, tunnel_wandb=None, tunnel_pushgateway=None,
            error=f"wandb tunnel 失败: {e}; {hint}",
        )

    # 2. 建 pushgateway tunnel (17891, 临时)
    try:
        host = _host_spec(spec)
        push_tunnel = _open_pushgateway_tunnel(host, PUSHGATEWAY_LOCAL_PORT)
    except Exception as e:
        # pushgateway tunnel 失败 -> warn, wandb 主路径仍可验
        emit_progress("reach.push.tunnel.fail", level="warn", server=server_name, error=str(e)[:200])

    try:
        # 3. wandb
        wandb_check = _check_wandb(spec)

        # 4. pushgateway (best-effort)
        push_check = _check_pushgateway(spec, push_tunnel)

        # 5. 汇总
        overall_ok = wandb_check["ok"]  # 主路径 wandb 通即 ok
        push_failed_but_warned = (not push_check["ok"]) and bool(push_check["warning"])

        if not wandb_check["ok"]:
            # wandb 失败 -> 整体 fail + 诊断
            hint = DIAG_HINT.format(alias=server_name)
            err = f"wandb 探测失败: {wandb_check.get('detail')}; {hint}"
            severity = "fail"
            overall_ok_final = False
        elif push_failed_but_warned:
            # wandb OK + push 失败 -> warn
            severity = "warn"
            err = None
            overall_ok_final = True
        else:
            severity = "ok"
            err = None
            overall_ok_final = True

        return ReachResult(
            server=server_name,
            ok=overall_ok_final,
            severity=severity,
            wandb=wandb_check,
            pushgateway=push_check,
            host=spec.host,
            tunnel_wandb=f"pid={tunnel_wandb_pid}, port={WANDB_REMOTE_PORT}",
            tunnel_pushgateway=(
                f"pid={push_tunnel.pid}, port={PUSHGATEWAY_REMOTE_PORT}"
                if push_tunnel else "unavailable"
            ),
            error=err,
        )
    finally:
        # 6. 收尾 push tunnel
        _close_pushgateway_tunnel(push_tunnel)
        emit_progress(
            "reach.test.result",
            level="info" if (wandb_check and wandb_check.get("ok")) else "warn",
            server=server_name,
        )


# === CLI boundary ===

def _check_message(severity: str, lang: str) -> str:
    if lang == "en":
        return {
            "ok": "Reach test passed",
            "warn": "Reach test passed with warnings",
            "fail": "Reach test failed",
        }.get(severity, "Reach test done")
    return {
        "ok": "可达性探测通过",
        "warn": "可达性探测通过 (含警告)",
        "fail": "可达性探测失败",
    }.get(severity, "可达性探测完成")


def run_reach_test(
    server: str,
    config: str | Path | None = None,
    lang: str = "zh",
) -> int:
    """CLI 边界: 单机 reach test, 输出 JSON, 走 __AR_PROGRESS__ 协议."""
    result = test_server_reach(server, config_path=config, lang=lang)
    payload = {
        "ok": result["ok"],
        "severity": result["severity"],
        "data": {
            "server": result["server"],
            "host": result["host"],
            "tunnel_wandb": result["tunnel_wandb"],
            "tunnel_pushgateway": result["tunnel_pushgateway"],
            "wandb": result["wandb"],
            "pushgateway": result["pushgateway"],
        },
        "message": _check_message(result["severity"], lang),
        "error": result["error"],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if result["ok"] else 1


# === --all multi-server ===

import sys as _sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import ReachSummary  # noqa: F401  (already imported at top)


def test_all_servers(
    config_path: str | Path | None = None,
    max_workers: int = 3,
    lang: str = "zh",
) -> ReachSummary:
    """并发跑全部 server reach test.

    复用 Phase 4 hw.probe.probe_all 模式: ThreadPoolExecutor + as_completed
    + worker exception 隔离. 结果按 config 顺序排.

    失败隔离 (D-07/D-29): 一台 worker 失败不取消其他.
    """
    from workspace_core.config import from_path
    cfg = from_path(str(config_path) if config_path else None)
    server_names = [s.name for s in cfg.servers]
    if not server_names:
        return ReachSummary(
            total=0, passed=0, failed=0, warned=0,
            passed_servers=[], failed_servers=[], results={},
        )
    worker_count = min(3, max_workers, len(server_names))
    results_by_name: dict[str, ReachResult] = {}
    with ThreadPoolExecutor(max_workers=worker_count) as ex:
        futures = {
            ex.submit(test_server_reach, name, config_path, lang): name
            for name in server_names
        }
        emit_progress("reach.all.begin", level="info", server=None)
        for future in as_completed(futures):
            name = futures[future]
            try:
                result: ReachResult = future.result()
            except Exception as exc:
                result = ReachResult(
                    server=name, ok=False, severity="fail",
                    wandb=ReachCheck(name="wandb", ok=False, latency_ms=None,
                                     status_code=None, detail=None, warning=None),
                    pushgateway=ReachCheck(name="pushgateway", ok=False, latency_ms=None,
                                           status_code=None, detail=None, warning=None),
                    host="", tunnel_wandb=None, tunnel_pushgateway=None,
                    error=f"worker 异常: {exc}",
                )
            results_by_name[name] = result
            emit_progress(
                "reach.all.complete" if result["ok"] else "reach.all.fail",
                level="info" if result["ok"] else "error",
                server=name,
                severity=result["severity"],
            )

    # 按 config 顺序
    ordered = {name: results_by_name[name] for name in server_names}
    passed = [n for n, r in ordered.items() if r["ok"]]
    failed = [n for n, r in ordered.items() if not r["ok"]]
    warned = sum(1 for r in ordered.values() if r["severity"] == "warn" and r["ok"])
    return ReachSummary(
        total=len(ordered),
        passed=len(passed),
        failed=len(failed),
        warned=warned,
        passed_servers=passed,
        failed_servers=failed,
        results=ordered,
    )


def run_reach_test_all(
    config: str | Path | None = None,
    lang: str = "zh",
) -> int:
    """CLI 边界: --all 多机 reach test, 输出汇总 JSON."""
    summary = test_all_servers(config_path=config, lang=lang)
    # 转成 CheckResult-ish 形态
    overall_ok = summary["failed"] == 0
    severity = "ok" if overall_ok else "fail"
    payload = {
        "ok": overall_ok,
        "severity": severity,
        "data": {
            "total": summary["total"],
            "passed": summary["passed"],
            "failed": summary["failed"],
            "warned": summary["warned"],
            "passed_servers": summary["passed_servers"],
            "failed_servers": summary["failed_servers"],
            "results": summary["results"],
        },
        "message": _check_message(severity, lang),
        "error": None if overall_ok else f"failed servers: {summary['failed_servers']}",
    }
    print(_sys_json_dumps(payload))
    return 0 if overall_ok else 1


def _sys_json_dumps(obj: dict) -> str:
    import json as _json
    return _json.dumps(obj, ensure_ascii=False)
