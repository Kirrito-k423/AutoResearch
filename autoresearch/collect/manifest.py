"""Build RunManifest objects from collection step results."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datalake.manifest import RunManifest
from workspace_core.config import ServerSpec


def build_manifest(
    run_id: str,
    spec: ServerSpec,
    lib: str,
    conda_env: str,
    workdir: str,
    minimal_result: dict[str, Any],
    wandb_path: Path | None,
    log_path: Path | None,
    prom_pushed: bool,
    *,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
    error: str | None = None,
    local_runs_root: Path | None = None,
) -> RunManifest:
    """Build the canonical local manifest for a minimal data-collection run."""
    root = Path(local_runs_root).expanduser() if local_runs_root else Path("~/.autoresearch/runs").expanduser()
    one_step = {
        "sum": minimal_result.get("sum_value"),
        "npu_count": minimal_result.get("npu_count"),
        "elapsed_ms": minimal_result.get("elapsed_ms"),
        "lib": minimal_result.get("lib", lib),
    }
    errors = [x for x in [minimal_result.get("error"), error] if x]
    return RunManifest(
        run_id=run_id,
        started_at=started_at or datetime.now(timezone.utc),
        finished_at=finished_at,
        server=spec.name,
        conda_env=conda_env,
        lib=lib,
        workdir_remote=workdir,
        workdir_local=root / run_id,
        one_step=one_step,
        exit_code=minimal_result.get("exit_code"),
        error="; ".join(errors) if errors else None,
        wandb_run_id=minimal_result.get("wandb_run_id"),
        wandb_path=wandb_path,
        log_files=[log_path] if log_path else [],
        prom_pushed=prom_pushed,
        prom_metrics_file=None,
    )
