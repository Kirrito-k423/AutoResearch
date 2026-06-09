"""Reusable reverse proxy tunnel lifecycle for network probes."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import signal
import shlex
import sys
import time
from urllib.parse import urlsplit, urlunsplit

from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.layout import LOGS_DIR, TUNNELS_DIR
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import HostSpec, resolve_host
from workspace_core.ssh.client import SSHClient
from workspace_core.ssh.exceptions import TunnelError
from workspace_core.ssh.tunnel import ReverseTunnel, open_reverse_tunnel

from .curl import build_curl_command, parse_curl_result, target_label
from .models import TunnelState


SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")
DEFAULT_LOCAL_PROXY_URL = "http://127.0.0.1:7890"
DEFAULT_REMOTE_PROXY_PORT = 17890
HEARTBEAT_INTERVAL_S = 30
RETRY_BACKOFF_S = (1, 2, 4)


def redact_proxy_url(url: str) -> str:
    """Redact proxy userinfo before state, JSON, or error text exposure."""
    parsed = urlsplit(url)
    if not parsed.netloc or "@" not in parsed.netloc:
        return url
    host = parsed.hostname or ""
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    if parsed.port is not None:
        host = f"{host}:{parsed.port}"
    return urlunsplit(
        (
            parsed.scheme,
            f"***:***@{host}",
            parsed.path,
            parsed.query,
            parsed.fragment,
        )
    )


def state_path_for(server_name: str) -> Path:
    """Return the sanitized local tunnel state path for one server."""
    safe_name = SAFE_NAME_RE.sub("_", server_name).strip("._") or "unknown"
    return TUNNELS_DIR / f"{safe_name}.json"


def load_tunnel_state(server_name: str) -> TunnelState | None:
    """Load tunnel state; missing or corrupt JSON is recoverable."""
    path = state_path_for(server_name)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    try:
        return TunnelState(
            server=str(data["server"]),
            pid=int(data["pid"]),
            remote_port=int(data["remote_port"]),
            local_proxy_url=str(data["local_proxy_url"]),
            remote_proxy_url=str(data["remote_proxy_url"]),
            started_at=str(data["started_at"]),
            log_path=(
                str(data["log_path"])
                if data.get("log_path") is not None
                else None
            ),
            last_heartbeat_at=(
                str(data["last_heartbeat_at"])
                if data.get("last_heartbeat_at") is not None
                else None
            ),
            last_heartbeat_ok=bool(data["last_heartbeat_ok"]),
            error=(
                str(data["error"])
                if data.get("error") is not None
                else None
            ),
        )
    except (KeyError, TypeError, ValueError):
        return None


def write_tunnel_state(state: TunnelState) -> Path:
    """Persist sanitized tunnel state under ~/.autoresearch/tunnels."""
    path = state_path_for(state["server"])
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_state = dict(state)
    safe_state["local_proxy_url"] = redact_proxy_url(
        safe_state["local_proxy_url"]
    )
    path.write_text(
        json.dumps(safe_state, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path


def delete_tunnel_state(server_name: str) -> None:
    """Remove one tunnel state file if it exists."""
    try:
        state_path_for(server_name).unlink()
    except FileNotFoundError:
        return


def resolve_server_host(
    server_name: str,
    config_path: str | Path | None = None,
) -> tuple[ServerSpec, HostSpec]:
    """Resolve an exact configured server name to a public SSH host spec."""
    config = from_path(config_path)
    server = next(
        (item for item in config.servers if item.name == server_name),
        None,
    )
    if server is None:
        available = [item.name for item in config.servers]
        raise ConfigError(
            f"config.servers 中找不到 '{server_name}'; 当前已配: {available}"
        )

    host = resolve_host(f"{server.user}@{server.host}:{server.port}")
    host = HostSpec(
        alias=server.name,
        host=host.host,
        port=host.port,
        user=host.user,
        identity_file=(
            Path(server.identity_file).expanduser()
            if server.identity_file
            else None
        ),
    )
    return server, host


def is_process_alive(pid: int) -> bool:
    """Return whether a local process appears alive."""
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def heartbeat_tunnel(
    server_name: str,
    state: TunnelState,
    config_path: str | Path | None = None,
    target_url: str | None = None,
    ssh_client_factory=SSHClient,
) -> bool:
    """Check local tunnel pid and remote proxy curl heartbeat."""
    emit_progress("net.tunnel.heartbeat", server=server_name)
    if not is_process_alive(state["pid"]):
        return False
    target = target_url or _heartbeat_target(config_path)
    server, host = resolve_server_host(server_name, config_path)
    client = None
    try:
        client = ssh_client_factory(
            host,
            bootstrap_password=server.bootstrap_password_secret,
        )
        client.connect(connect_timeout=5.0)
        exit_code, stdout, stderr = client.exec(
            _remote_proxy_curl_command(target, state["remote_proxy_url"]),
            timeout=12,
        )
        attempt = parse_curl_result(
            exit_code,
            stdout,
            stderr,
            "proxy",
            target,
            proxy_url=state["remote_proxy_url"],
        )
        return attempt["ok"]
    except Exception:
        return False
    finally:
        if client is not None:
            client.close()


def ensure_tunnel(
    server_name: str,
    config_path: str | Path | None = None,
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    tunnel_opener=open_reverse_tunnel,
    heartbeat_fn=heartbeat_tunnel,
    sleep_fn=time.sleep,
    max_retries: int = 3,
) -> TunnelState:
    """Create, reuse, or rebuild a reverse tunnel for remote proxy retry."""
    local_port = _local_proxy_port(local_proxy_url)
    remote_proxy_url = f"http://127.0.0.1:{remote_proxy_port}"
    state = load_tunnel_state(server_name)
    if (
        state is not None
        and state["remote_port"] == remote_proxy_port
        and state["local_proxy_url"] == redact_proxy_url(local_proxy_url)
        and is_process_alive(state["pid"])
    ):
        heartbeat_ok = heartbeat_fn(server_name, state, config_path)
        refreshed = _with_heartbeat(state, heartbeat_ok, None)
        write_tunnel_state(refreshed)
        if heartbeat_ok:
            emit_progress("net.tunnel.ready", server=server_name)
            return refreshed

    if state is not None and state["pid"] > 0 and is_process_alive(state["pid"]):
        _stop_process(state["pid"])
    delete_tunnel_state(server_name)

    _, host = resolve_server_host(server_name, config_path)
    attempts = max(1, max_retries + 1)
    last_error = "heartbeat failed"
    for attempt_index in range(attempts):
        try:
            tunnel: ReverseTunnel = tunnel_opener(
                host,
                remote_port=remote_proxy_port,
                local_port=local_port,
                identity_file=host.identity_file,
                log_dir=LOGS_DIR,
            )
            new_state = TunnelState(
                server=server_name,
                pid=tunnel.pid,
                remote_port=remote_proxy_port,
                local_proxy_url=redact_proxy_url(local_proxy_url),
                remote_proxy_url=remote_proxy_url,
                started_at=_now(),
                log_path=str(tunnel.log_path),
                last_heartbeat_at=None,
                last_heartbeat_ok=False,
                error=None,
            )
            heartbeat_ok = heartbeat_fn(server_name, new_state, config_path)
            new_state = _with_heartbeat(new_state, heartbeat_ok, None)
            write_tunnel_state(new_state)
            if heartbeat_ok:
                emit_progress("net.tunnel.ready", server=server_name)
                return new_state
            _stop_process(new_state["pid"])
            last_error = "heartbeat failed"
        except TunnelError as exc:
            last_error = _sanitize_error(str(exc), local_proxy_url)

        if attempt_index < attempts - 1:
            delay = RETRY_BACKOFF_S[min(attempt_index, len(RETRY_BACKOFF_S) - 1)]
            emit_progress(
                "net.tunnel.retry",
                level="warn",
                server=server_name,
                attempt=attempt_index + 1,
                delay_s=delay,
            )
            sleep_fn(delay)

    failed_state = TunnelState(
        server=server_name,
        pid=0,
        remote_port=remote_proxy_port,
        local_proxy_url=redact_proxy_url(local_proxy_url),
        remote_proxy_url=remote_proxy_url,
        started_at=_now(),
        log_path=None,
        last_heartbeat_at=_now(),
        last_heartbeat_ok=False,
        error=_sanitize_error(last_error, local_proxy_url),
    )
    write_tunnel_state(failed_state)
    emit_progress("net.tunnel.fail", level="error", server=server_name)
    raise TunnelError(failed_state["error"] or "tunnel heartbeat failed")


def run_tunnel_ensure(
    server: str,
    config: str | Path | None = None,
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    lang: str = "zh",
) -> int:
    """CLI boundary: ensure one tunnel and print exactly one JSON object."""
    emit_progress("net.tunnel.ensure.start", server=server)
    try:
        state = ensure_tunnel(
            server,
            config_path=config,
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
        )
        result = CheckResult(
            ok=True,
            severity=CheckSeverity.OK,
            data={
                "server": state["server"],
                "remote_proxy_url": state["remote_proxy_url"],
                "remote_port": state["remote_port"],
                "pid": state["pid"],
                "log_path": state["log_path"],
                "last_heartbeat_ok": state["last_heartbeat_ok"],
            },
            message="隧道已就绪" if lang == "zh" else "Tunnel ready",
            error=None,
        )
        exit_code = 0
    except ConfigError as exc:
        result = _tunnel_failure(
            "配置错误" if lang == "zh" else "Config error",
            str(exc),
        )
        exit_code = 2
    except Exception as exc:
        result = _tunnel_failure(
            "隧道建立失败" if lang == "zh" else "Tunnel ensure failed",
            _sanitize_error(str(exc), local_proxy_url),
        )
        exit_code = 1

    if result["error"]:
        print(f"{result['message']}: {result['error']}", file=sys.stderr)
    emit_progress(
        "net.tunnel.ensure.result",
        level="info" if result["ok"] else "error",
        server=server,
        severity=result["severity"].value,
    )
    print(json.dumps(result, ensure_ascii=False))
    return exit_code


def _local_proxy_port(local_proxy_url: str) -> int:
    parsed = urlsplit(local_proxy_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ConfigError("local proxy URL 必须是 http(s)://localhost:PORT")
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ConfigError("local proxy URL 只允许 localhost/127.0.0.1")
    if parsed.port is None:
        raise ConfigError("local proxy URL 必须显式包含端口")
    return parsed.port


def _stop_process(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _sanitize_error(error: str, local_proxy_url: str) -> str:
    text = error.replace(local_proxy_url, redact_proxy_url(local_proxy_url))
    return " ".join(text.split())[:500]


def _with_heartbeat(
    state: TunnelState,
    ok: bool,
    error: str | None,
) -> TunnelState:
    return TunnelState(
        **{
            **state,
            "last_heartbeat_at": _now(),
            "last_heartbeat_ok": ok,
            "error": None if ok else (error or "heartbeat failed"),
        }
    )


def _heartbeat_target(config_path: str | Path | None) -> str:
    config = from_path(config_path)
    targets = list(config.network.targets)
    if not targets:
        raise ConfigError("config.network.targets 不能为空")
    for url in targets:
        if target_label(url) == "baidu":
            return url
    return targets[0]


def _remote_proxy_curl_command(url: str, proxy_url: str) -> str:
    command = build_curl_command(url, timeout_s=5)
    proxy = shlex.quote(proxy_url)
    shell_command = " ".join(shlex.quote(part) for part in command)
    return f"ALL_PROXY={proxy} HTTPS_PROXY={proxy} {shell_command}"


def _tunnel_failure(message: str, error: str) -> CheckResult:
    return CheckResult(
        ok=False,
        severity=CheckSeverity.FAIL,
        data={},
        message=message,
        error=error,
    )
