"""Reusable reverse proxy tunnel lifecycle for network probes."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import signal
from urllib.parse import urlsplit, urlunsplit

from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.layout import LOGS_DIR, TUNNELS_DIR
from workspace_core.ssh import HostSpec, resolve_host
from workspace_core.ssh.exceptions import TunnelError
from workspace_core.ssh.tunnel import ReverseTunnel, open_reverse_tunnel

from .models import TunnelState


SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")
DEFAULT_LOCAL_PROXY_URL = "http://127.0.0.1:7890"
DEFAULT_REMOTE_PROXY_PORT = 17890


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


def heartbeat_tunnel(state: TunnelState) -> bool:
    """05-02 baseline heartbeat: verify the local ssh process is alive."""
    return is_process_alive(state["pid"])


def ensure_tunnel(
    server_name: str,
    config_path: str | Path | None = None,
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    tunnel_opener=open_reverse_tunnel,
) -> TunnelState:
    """Create, reuse, or rebuild a reverse tunnel for remote proxy retry."""
    local_port = _local_proxy_port(local_proxy_url)
    remote_proxy_url = f"http://127.0.0.1:{remote_proxy_port}"
    state = load_tunnel_state(server_name)
    if (
        state is not None
        and state["remote_port"] == remote_proxy_port
        and state["local_proxy_url"] == redact_proxy_url(local_proxy_url)
        and heartbeat_tunnel(state)
    ):
        refreshed = TunnelState(
            **{
                **state,
                "last_heartbeat_at": _now(),
                "last_heartbeat_ok": True,
                "error": None,
            }
        )
        write_tunnel_state(refreshed)
        return refreshed

    if state is not None and state["pid"] > 0 and is_process_alive(state["pid"]):
        _stop_process(state["pid"])
    delete_tunnel_state(server_name)

    _, host = resolve_server_host(server_name, config_path)
    try:
        tunnel: ReverseTunnel = tunnel_opener(
            host,
            remote_port=remote_proxy_port,
            local_port=local_port,
            identity_file=host.identity_file,
            log_dir=LOGS_DIR,
        )
    except TunnelError as exc:
        raise TunnelError(_sanitize_error(str(exc), local_proxy_url)) from exc

    new_state = TunnelState(
        server=server_name,
        pid=tunnel.pid,
        remote_port=remote_proxy_port,
        local_proxy_url=redact_proxy_url(local_proxy_url),
        remote_proxy_url=remote_proxy_url,
        started_at=_now(),
        log_path=str(tunnel.log_path),
        last_heartbeat_at=_now(),
        last_heartbeat_ok=True,
        error=None,
    )
    write_tunnel_state(new_state)
    return new_state


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
