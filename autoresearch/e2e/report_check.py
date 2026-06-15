"""Report completeness checks for E2E smoke runs."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from autoresearch.report.loader import load_report_bundle


DEFAULT_PROMETHEUS_URL = "http://localhost:9090"


def check_report_completeness(
    *,
    run_id: str,
    runs_root: Path | None = None,
    prometheus_url: str = DEFAULT_PROMETHEUS_URL,
) -> tuple[int, dict[str, Any]]:
    """Verify that a rendered report has log, wandb, and Prometheus views."""
    try:
        bundle = load_report_bundle(
            run_id,
            root=runs_root,
            prometheus_base_url=prometheus_url,
        )
    except Exception as exc:
        return 1, {
            "ok": False,
            "run_id": run_id,
            "error": str(exc),
            "checks": {},
            "missing": ["bundle"],
            "warnings": [],
        }

    report_path = bundle.manifest_path.parent / "report.html"
    checks = {
        "html": {
            "ok": report_path.exists(),
            "path": str(report_path),
            "warning": None if report_path.exists() else "report.html missing",
        },
        "log": {
            "ok": bundle.log.available,
            "path": str(bundle.log.path) if bundle.log.path else None,
            "warning": bundle.log.warning,
        },
        "wandb": {
            "ok": bundle.wandb.available,
            "path": str(bundle.wandb.local_path) if bundle.wandb.local_path else None,
            "warning": bundle.wandb.warning,
        },
        "prometheus": {
            "ok": bundle.prometheus.available,
            "query": bundle.prometheus.query,
            "warning": bundle.prometheus.warning,
        },
    }
    missing = [name for name, item in checks.items() if not item["ok"]]
    payload = {
        "ok": not missing,
        "run_id": run_id,
        "report": str(report_path),
        "checks": checks,
        "missing": missing,
        "warnings": list(bundle.warnings),
    }
    return (0 if payload["ok"] else 1), payload
