"""Push minimal run metrics to a reachable Prometheus Pushgateway."""
from __future__ import annotations

import re
import shlex
import importlib
from pathlib import Path

from workspace_core.config import ServerSpec
from workspace_core.ssh import HostSpec
from workspace_core.ssh.tunnel import open_reverse_tunnel

run_in_env = importlib.import_module("workspace-adapter.common.conda_utils").run_in_env

PUSHGATEWAY_REMOTE_PORT = 17891
PUSHGATEWAY_LOCAL_PORT = 9091


class PushError(Exception):
    """Pushgateway write failed."""


def _job_suffix(run_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", run_id).strip("_")
    return cleaned or "unknown"


def push_metrics(
    server: ServerSpec,
    run_id: str,
    npu_count: int,
    pushgateway_url: str = "http://localhost:9091",
    timeout: float = 10.0,
) -> bool:
    """Push one NPU-count metric from the remote server.

    Uses Pushgateway's text exposition endpoint through ``curl`` so the remote
    conda env does not need the prometheus_client package.
    """
    if not run_id:
        raise PushError("run_id 不能为空")
    if npu_count < 0:
        raise PushError("npu_count 不能为负数")

    endpoint = f"{pushgateway_url.rstrip('/')}/metrics/job/ar_{_job_suffix(run_id)}"
    metric = f'autoresearch_npu_count{{run_id="{_job_suffix(run_id)}"}} {int(npu_count)}\n'
    command = (
        f"printf %s {shlex.quote(metric)} "
        f"| curl --fail --silent --show-error --data-binary @- {shlex.quote(endpoint)}"
    )
    tunnel = _open_pushgateway_tunnel(server)
    try:
        ec, stdout, stderr = run_in_env(
            server,
            command,
            conda_env=getattr(server, "conda_env", "") or "",
            workdir=getattr(server, "workdir", "/root") or "/root",
            timeout=timeout,
        )
    finally:
        tunnel.stop(timeout_s=3.0)
    if ec != 0:
        detail = (stderr or stdout or "").strip()
        raise PushError(f"pushgateway 推送失败 exit={ec}: {detail[:200]}")
    return True


def _open_pushgateway_tunnel(server: ServerSpec):
    identity_file = getattr(server, "identity_file", None)
    host = HostSpec(
        alias=server.name,
        host=server.host,
        port=int(server.port),
        user=server.user,
        identity_file=identity_file,
    )
    return open_reverse_tunnel(
        host,
        remote_port=PUSHGATEWAY_REMOTE_PORT,
        local_port=PUSHGATEWAY_LOCAL_PORT,
        identity_file=Path(identity_file).expanduser() if identity_file else None,
    )
