"""Push minimal run metrics to a reachable Prometheus Pushgateway."""
from __future__ import annotations

import re
import shlex

from workspace_core.config import ServerSpec
from verl_workspace_adapter.common.conda_utils import run_in_env


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
    ec, stdout, stderr = run_in_env(
        server,
        command,
        conda_env=getattr(server, "conda_env", "") or "",
        workdir=getattr(server, "workdir", "/root") or "/root",
        timeout=timeout,
    )
    if ec != 0:
        detail = (stderr or stdout or "").strip()
        raise PushError(f"pushgateway 推送失败 exit={ec}: {detail[:200]}")
    return True
