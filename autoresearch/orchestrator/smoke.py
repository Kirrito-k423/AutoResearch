"""Implementation for `autoresearch run smoke`."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from workspace_core.progress import emit_progress

from autoresearch.collect.cli import run_collect
from autoresearch.report.prometheus import build_prom_query
from autoresearch.report.cli import run_render

from .models import StepResult, skipped_step, step_result, summarize_steps


DEFAULT_PUSHGATEWAY_URL = "http://127.0.0.1:17891"
DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_PROMETHEUS_WAIT = 16.0


def run_smoke(
    *,
    server: str,
    lib: str = "verl",
    config: str | None = None,
    workdir: str | None = None,
    timeout: float = 60.0,
    run_id: str | None = None,
    pushgateway_url: str = DEFAULT_PUSHGATEWAY_URL,
    prometheus_url: str = DEFAULT_PROMETHEUS_URL,
    prometheus_wait: float = DEFAULT_PROMETHEUS_WAIT,
    open_report: bool = False,
    runs_root: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    """Run collect -> report and return one orchestration payload."""
    emit_progress("orch.smoke.start", server=server, lib=lib)
    steps: list[StepResult] = []

    emit_progress("orch.smoke.step.start", step="collect")
    try:
        collect_exit, collect_payload = run_collect(
            server=server,
            lib=lib,
            config=config,
            workdir=workdir,
            timeout=timeout,
            run_id=run_id,
            pushgateway_url=pushgateway_url,
            local_runs_root=runs_root,
        )
    except Exception as exc:
        collect_exit, collect_payload = 2, {"ok": False, "error": str(exc)}
    collect_step = step_result(
        step_id="collect",
        label="data-collection",
        exit_code=collect_exit,
        payload=collect_payload,
    )
    steps.append(collect_step)
    emit_progress(
        "orch.smoke.step.result",
        level="error" if collect_step["status"] == "fail" else "info",
        step="collect",
        status=collect_step["status"],
    )

    report_payload: dict[str, Any] | None = None
    prometheus_ready: bool | None = None
    if not collect_step["ok"]:
        steps.append(
            skipped_step(
                "report",
                "experiment-report",
                "collect step failed; no run_id available for report render",
            )
        )
    else:
        rid = collect_payload.get("run_id")
        if not rid:
            report_step = step_result(
                step_id="report",
                label="experiment-report",
                exit_code=1,
                payload={
                    "ok": False,
                    "error": "collect step succeeded but did not return run_id",
                },
            )
            steps.append(report_step)
            emit_progress(
                "orch.smoke.step.result",
                level="error",
                step="report",
                status=report_step["status"],
            )
        else:
            rid_text = str(rid)
            if collect_payload.get("prom_pushed") and prometheus_wait > 0:
                emit_progress(
                    "orch.smoke.prometheus.wait",
                    run_id=rid_text,
                    timeout_seconds=prometheus_wait,
                )
                prometheus_ready = _wait_for_prometheus_metric(
                    rid_text,
                    base_url=prometheus_url,
                    timeout=prometheus_wait,
                )
                emit_progress(
                    "orch.smoke.prometheus.result",
                    level="info" if prometheus_ready else "warn",
                    run_id=rid_text,
                    ready=prometheus_ready,
                )
            emit_progress("orch.smoke.step.start", step="report", run_id=rid_text)
            try:
                report_exit, report_payload = run_render(
                    run_id=rid_text,
                    open_report=open_report,
                    runs_root=runs_root,
                )
            except Exception as exc:
                report_exit, report_payload = 1, {"ok": False, "run_id": rid_text, "error": str(exc)}
            report_step = step_result(
                step_id="report",
                label="experiment-report",
                exit_code=report_exit,
                payload=report_payload,
            )
            steps.append(report_step)
            emit_progress(
                "orch.smoke.step.result",
                level="error" if report_step["status"] == "fail" else "info",
                step="report",
                status=report_step["status"],
            )

    summary = summarize_steps(steps)
    ok = summary["failed"] == 0
    payload = {
        "ok": ok,
        "command": "smoke",
        "server": server,
        "lib": lib,
        "run_id": collect_payload.get("run_id"),
        "manifest": collect_payload.get("manifest"),
        "report": report_payload.get("report") if report_payload else None,
        "prometheus_ready": prometheus_ready,
        "failed_step": summary["failed_step"],
        "summary": summary,
        "steps": steps,
    }
    emit_progress(
        "orch.smoke.result",
        level="info" if ok else "error",
        ok=ok,
        failed_step=summary["failed_step"],
    )
    return (0 if ok else 1), payload


def _wait_for_prometheus_metric(
    run_id: str,
    *,
    base_url: str,
    timeout: float,
) -> bool:
    deadline = time.monotonic() + timeout
    while True:
        if _prometheus_has_metric(run_id, base_url=base_url):
            return True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(1.0, remaining))


def _prometheus_has_metric(run_id: str, *, base_url: str) -> bool:
    params = urlencode({"query": build_prom_query(run_id)})
    url = f"{base_url.rstrip('/')}/api/v1/query?{params}"
    try:
        with urlopen(url, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        return False
    return bool(data.get("data", {}).get("result"))
