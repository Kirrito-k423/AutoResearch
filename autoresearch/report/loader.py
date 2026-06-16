"""Load local report data from manifest, logs, wandb, and Prometheus."""
from __future__ import annotations

from pathlib import Path

from datalake.manifest import RunManifest
from workspace_core.layout.paths import RUNS_DIR, run_dir

from .logs import load_log_view
from .models import ArtifactLink, ReportBundle
from .prometheus import build_prom_query_url, load_prometheus_view
from .verl_case import load_verl_case_view
from .wandb import load_wandb_view


def _manifest_path(run_id: str, root: Path | None) -> Path:
    if root is not None:
        return Path(root).expanduser() / run_id / "manifest.json"
    return run_dir(run_id, create=False).manifest


def load_report_bundle(
    run_id: str,
    *,
    root: Path | None = None,
    wandb_base_url: str = "http://localhost:8080",
    prometheus_base_url: str = "http://localhost:9090",
) -> ReportBundle:
    """Load the normalized report payload for one collected run."""
    manifest_path = _manifest_path(run_id, root)
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest 不存在: {manifest_path}")

    manifest = RunManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )

    log_view = load_log_view(manifest)
    wandb_view = load_wandb_view(manifest, base_url=wandb_base_url)
    prom_view = load_prometheus_view(manifest, base_url=prometheus_base_url)
    formal_case_view = load_verl_case_view(manifest, manifest_path=manifest_path)

    warnings = [
        warning
        for warning in (log_view.warning, wandb_view.warning, prom_view.warning)
        if warning
    ]
    if formal_case_view:
        warnings.extend(formal_case_view.warnings)
    artifact_links = [ArtifactLink(label="manifest.json", href=manifest_path.as_uri())]
    if log_view.path is not None:
        artifact_links.append(ArtifactLink(label="log.txt", href=log_view.path.as_uri()))
    if wandb_view.local_path is not None:
        artifact_links.append(
            ArtifactLink(label="wandb artifact dir", href=wandb_view.local_path.as_uri())
        )
    artifact_links.append(
        ArtifactLink(
            label="Prometheus query",
            href=build_prom_query_url(manifest.run_id, base_url=prometheus_base_url),
            note=manifest.run_id,
        )
    )
    if formal_case_view:
        for artifact in formal_case_view.artifacts:
            if artifact.path is not None and artifact.path.exists():
                artifact_links.append(
                    ArtifactLink(
                        label=artifact.name,
                        href=artifact.path.as_uri(),
                    )
                )

    return ReportBundle(
        run_id=manifest.run_id,
        manifest_path=manifest_path,
        started_at=manifest.started_at,
        finished_at=manifest.finished_at,
        server=manifest.server,
        conda_env=manifest.conda_env,
        lib=manifest.lib,
        workdir_remote=manifest.workdir_remote,
        workdir_local=manifest.workdir_local,
        exit_code=manifest.exit_code,
        error=manifest.error,
        one_step=manifest.one_step,
        artifact_links=artifact_links,
        warnings=warnings,
        log=log_view,
        wandb=wandb_view,
        prometheus=prom_view,
        formal_case=formal_case_view,
    )
