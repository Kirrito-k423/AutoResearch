"""Shared result helpers for top-level orchestration."""
from __future__ import annotations

from typing import Any, Literal, TypedDict


StepStatus = Literal["pass", "warn", "fail", "skipped"]


class StepResult(TypedDict):
    id: str
    label: str
    ok: bool
    status: StepStatus
    exit_code: int | None
    diagnosis: str | None
    payload: dict[str, Any]


def step_result(
    *,
    step_id: str,
    label: str,
    exit_code: int,
    payload: dict[str, Any],
) -> StepResult:
    """Normalize a skill result into the orchestrator step schema."""
    payload_ok = payload.get("ok")
    severity = payload.get("severity")
    if exit_code == 0 and payload_ok is not False:
        status: StepStatus = "warn" if severity == "warn" else "pass"
        ok = True
    else:
        status = "fail"
        ok = False
    return {
        "id": step_id,
        "label": label,
        "ok": ok,
        "status": status,
        "exit_code": exit_code,
        "diagnosis": _diagnosis(payload),
        "payload": payload,
    }


def ready_step(step_id: str, label: str, message: str) -> StepResult:
    """Create a deterministic readiness step that does not run a mutating action."""
    return {
        "id": step_id,
        "label": label,
        "ok": True,
        "status": "pass",
        "exit_code": 0,
        "diagnosis": None,
        "payload": {"ok": True, "message": message},
    }


def skipped_step(step_id: str, label: str, reason: str) -> StepResult:
    """Create a skipped step with an explicit reason."""
    return {
        "id": step_id,
        "label": label,
        "ok": True,
        "status": "skipped",
        "exit_code": None,
        "diagnosis": reason,
        "payload": {"ok": None, "skipped": True, "reason": reason},
    }


def summarize_steps(steps: list[StepResult]) -> dict[str, Any]:
    """Build a compact summary and first failed step marker."""
    counts = {"passed": 0, "warned": 0, "failed": 0, "skipped": 0}
    failed_step = None
    for step in steps:
        if step["status"] == "pass":
            counts["passed"] += 1
        elif step["status"] == "warn":
            counts["warned"] += 1
        elif step["status"] == "fail":
            counts["failed"] += 1
            failed_step = failed_step or step["id"]
        elif step["status"] == "skipped":
            counts["skipped"] += 1
    return {
        "total": len(steps),
        **counts,
        "failed_step": failed_step,
    }


def _diagnosis(payload: dict[str, Any]) -> str | None:
    if payload.get("error"):
        return str(payload["error"])
    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        return "; ".join(str(item) for item in errors[:3])
    missing = payload.get("missing")
    if isinstance(missing, list) and missing:
        return "missing: " + ", ".join(str(item) for item in missing[:5])
    if payload.get("message") and payload.get("ok") is False:
        return str(payload["message"])
    summary = payload.get("summary")
    if isinstance(summary, dict) and summary.get("unhealthy"):
        return f"{summary['unhealthy']} service(s) unhealthy"
    return None
