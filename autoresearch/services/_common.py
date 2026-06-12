"""Common helpers for autoresearch.services subcommands.

SVC-CHK-STAT-01..03: 4 services, concurrent healthz, machine-readable JSON.
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict

import requests


class HealthResult(TypedDict):
    """Per-service health check result."""

    name: str
    url: str
    healthy: bool
    latency_ms: int
    error: str | None


# 4 services fixed (D-03c); 端口可用环境变量覆盖（默认 .env.example）
# 注意：archon 端口固定 8088（D-05 锁定，不在 compose 里）
# 5 services fixed (D-03c); 端口可用环境变量覆盖（默认 .env.example）
# 注意：archon 端口固定 8088（D-05 锁定，不在 compose 里）
# pushgateway 是 Phase 06-01 引入 (D-36), 端口 9091
SERVICES: list[tuple[str, str]] = [
    ("archon", "http://localhost:8088/healthz"),
    ("wandb", "http://localhost:8080/healthz"),
    ("prometheus", "http://localhost:9090/-/healthy"),
    ("grafana", "http://localhost:3000/api/health"),
    ("pushgateway", "http://localhost:9091/-/healthy"),
]

DEFAULT_TIMEOUT_S = 3.0


def check_one(name: str, url: str, timeout: float = DEFAULT_TIMEOUT_S) -> HealthResult:
    """Probe a single service's health endpoint.

    Returns a HealthResult dict; never raises.
    """
    t0 = time.perf_counter()
    try:
        resp = requests.get(url, timeout=timeout)
        latency_ms = int((time.perf_counter() - t0) * 1000)
        return HealthResult(
            name=name,
            url=url,
            healthy=resp.ok,
            latency_ms=latency_ms,
            error=None if resp.ok else f"HTTP {resp.status_code}",
        )
    except requests.RequestException as e:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        return HealthResult(
            name=name,
            url=url,
            healthy=False,
            latency_ms=latency_ms,
            error=str(e),
        )


def check_all(timeout: float = DEFAULT_TIMEOUT_S) -> list[HealthResult]:
    """Concurrently probe all 4 services.

    Uses ThreadPoolExecutor with 4 workers (one per service) — order is preserved
    via the result iterator.
    """
    with ThreadPoolExecutor(max_workers=len(SERVICES)) as ex:
        return list(ex.map(lambda s: check_one(s[0], s[1], timeout), SERVICES))
