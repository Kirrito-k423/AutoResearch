"""Implementation for `autoresearch e2e smoke`."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable
from urllib.error import URLError
from urllib.request import urlopen

from workspace_core.progress import emit_progress

from autoresearch.orchestrator.checks import (
    DEFAULT_REMOTE_PROXY_PORT,
    run_check_all,
)
from autoresearch.orchestrator.models import (
    StepResult,
    skipped_step,
    step_result,
    summarize_steps,
)
from autoresearch.orchestrator.smoke import (
    DEFAULT_PROMETHEUS_URL,
    DEFAULT_PROMETHEUS_WAIT,
    DEFAULT_PUSHGATEWAY_URL,
    run_smoke,
)

from .report_check import check_report_completeness


DEFAULT_ARCHON_URL = "http://localhost:8088"
DEFAULT_MAX_DURATION = 1800.0
DEFAULT_WORKFLOW_PATH = ".archon/workflows/ar-min-loop.yaml"


def run_e2e_smoke(
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
    archon_url: str = DEFAULT_ARCHON_URL,
    max_duration: float = DEFAULT_MAX_DURATION,
    open_report: bool = False,
    runs_root: Path | None = None,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    lang: str = "zh",
) -> tuple[int, dict[str, Any]]:
    """Run readiness -> smoke -> report completeness -> observability gates."""
    started = time.monotonic()
    emit_progress("e2e.smoke.start", server=server, lib=lib)
    steps: list[StepResult] = []

    readiness = _run_step(
        "readiness",
        "check-all-readiness",
        lambda: run_check_all(
            server=server,
            config=config,
            stack_libs=(lib,),
            remote_proxy_port=remote_proxy_port,
            lang=lang,
        ),
    )
    steps.append(readiness)
    if not readiness["ok"]:
        steps.extend(_skip_after("readiness check failed"))
        return _finish(steps, started, server, lib)

    smoke = _run_step(
        "smoke",
        "collect-and-report",
        lambda: run_smoke(
            server=server,
            lib=lib,
            config=config,
            workdir=workdir,
            timeout=timeout,
            run_id=run_id,
            pushgateway_url=pushgateway_url,
            prometheus_url=prometheus_url,
            prometheus_wait=prometheus_wait,
            open_report=open_report,
            runs_root=runs_root,
        ),
    )
    steps.append(smoke)
    if not smoke["ok"]:
        steps.extend(_skip_after("smoke run failed", start_at="report"))
        return _finish(steps, started, server, lib)

    smoke_run_id = smoke["payload"].get("run_id")
    if not smoke_run_id:
        report = step_result(
            step_id="report",
            label="report-completeness",
            exit_code=1,
            payload={"ok": False, "error": "smoke step did not return run_id"},
        )
        emit_progress("e2e.smoke.step.result", level="error", step="report", status="fail")
    else:
        report = _run_step(
            "report",
            "report-completeness",
            lambda: check_report_completeness(
                run_id=str(smoke_run_id),
                runs_root=runs_root,
                prometheus_url=prometheus_url,
            ),
        )
    steps.append(report)
    if not report["ok"]:
        steps.extend(_skip_after("report completeness failed", start_at="archon"))
        return _finish(steps, started, server, lib)

    archon = _run_step(
        "archon",
        "archon-observability",
        lambda: _check_archon_observable(archon_url=archon_url),
    )
    steps.append(archon)
    if not archon["ok"]:
        steps.append(skipped_step("duration", "duration-gate", "archon observability failed"))
        return _finish(steps, started, server, lib)

    emit_progress("e2e.smoke.step.start", step="duration")
    elapsed = time.monotonic() - started
    duration = step_result(
        step_id="duration",
        label="duration-gate",
        exit_code=0 if elapsed <= max_duration else 1,
        payload={
            "ok": elapsed <= max_duration,
            "elapsed_seconds": round(elapsed, 3),
            "max_duration_seconds": max_duration,
        },
    )
    emit_progress(
        "e2e.smoke.step.result",
        level="info" if duration["ok"] else "error",
        step="duration",
        status=duration["status"],
    )
    steps.append(duration)
    return _finish(steps, started, server, lib)


def _run_step(
    step_id: str,
    label: str,
    fn: Callable[[], tuple[int, dict[str, Any]]],
) -> StepResult:
    emit_progress("e2e.smoke.step.start", step=step_id)
    try:
        exit_code, payload = fn()
    except Exception as exc:
        exit_code, payload = 2, {"ok": False, "error": str(exc)}
    step = step_result(
        step_id=step_id,
        label=label,
        exit_code=exit_code,
        payload=payload,
    )
    emit_progress(
        "e2e.smoke.step.result",
        level="error" if step["status"] == "fail" else "info",
        step=step_id,
        status=step["status"],
    )
    return step


def _check_archon_observable(
    *,
    archon_url: str = DEFAULT_ARCHON_URL,
    workflow_path: str | Path = DEFAULT_WORKFLOW_PATH,
) -> tuple[int, dict[str, Any]]:
    health_url = f"{archon_url.rstrip('/')}/healthz"
    health_ok = False
    status_code: int | None = None
    error: str | None = None
    try:
        with urlopen(health_url, timeout=2.0) as resp:
            status_code = getattr(resp, "status", None)
            health_ok = status_code is None or 200 <= status_code < 300
    except (URLError, TimeoutError, OSError) as exc:
        error = str(exc)

    workflow = Path(workflow_path)
    workflow_ok = workflow.exists()
    payload = {
        "ok": health_ok and workflow_ok,
        "health_url": health_url,
        "status_code": status_code,
        "workflow": str(workflow),
        "workflow_exists": workflow_ok,
        "error": error if not health_ok else None,
    }
    if not workflow_ok:
        payload["missing"] = ["ar-min-loop workflow"]
    return (0 if payload["ok"] else 1), payload


def _skip_after(reason: str, *, start_at: str = "smoke") -> list[StepResult]:
    order = ["smoke", "report", "archon", "duration"]
    labels = {
        "smoke": "collect-and-report",
        "report": "report-completeness",
        "archon": "archon-observability",
        "duration": "duration-gate",
    }
    start_index = order.index(start_at)
    return [skipped_step(step_id, labels[step_id], reason) for step_id in order[start_index:]]


def _finish(
    steps: list[StepResult],
    started: float,
    server: str,
    lib: str,
) -> tuple[int, dict[str, Any]]:
    elapsed = time.monotonic() - started
    summary = summarize_steps(steps)
    ok = summary["failed"] == 0
    smoke_payload = next((step["payload"] for step in steps if step["id"] == "smoke"), {})
    report_payload = next((step["payload"] for step in steps if step["id"] == "report"), {})
    payload = {
        "ok": ok,
        "command": "e2e-smoke",
        "server": server,
        "lib": lib,
        "run_id": smoke_payload.get("run_id"),
        "report": report_payload.get("report") or smoke_payload.get("report"),
        "failed_step": summary["failed_step"],
        "elapsed_seconds": round(elapsed, 3),
        "summary": summary,
        "steps": steps,
    }
    emit_progress(
        "e2e.smoke.result",
        level="info" if ok else "error",
        ok=ok,
        failed_step=summary["failed_step"],
        elapsed_seconds=payload["elapsed_seconds"],
    )
    return (0 if ok else 1), payload
