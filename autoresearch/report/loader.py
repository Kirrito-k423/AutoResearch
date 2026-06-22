"""Load local report data from manifest, logs, wandb, and Prometheus."""
from __future__ import annotations

from pathlib import Path

from datalake.manifest import RunManifest
from workspace_core.layout.paths import run_dir

from .logs import load_log_view
from .models import ArtifactLink, ReportBundle, SkillUsage
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
    return load_report_bundle_from_manifest(
        manifest_path,
        wandb_base_url=wandb_base_url,
        prometheus_base_url=prometheus_base_url,
    )


def load_report_bundle_from_manifest(
    manifest_path: Path,
    *,
    wandb_base_url: str = "http://localhost:8080",
    prometheus_base_url: str = "http://localhost:9090",
) -> ReportBundle:
    """Load the normalized report payload from an explicit manifest path."""
    manifest_path = Path(manifest_path).expanduser()
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest 不存在: {manifest_path}")

    manifest = RunManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )

    base_dir = manifest_path.parent
    log_view = load_log_view(manifest, base_dir=base_dir)
    wandb_view = load_wandb_view(manifest, base_url=wandb_base_url, base_dir=base_dir)
    prom_view = load_prometheus_view(manifest, base_url=prometheus_base_url, base_dir=base_dir)
    formal_case_view = load_verl_case_view(manifest, manifest_path=manifest_path)

    warnings = [
        warning
        for warning in (log_view.warning, wandb_view.warning, prom_view.warning)
        if warning
    ]
    if formal_case_view:
        warnings.extend(formal_case_view.warnings)
    artifact_links = [ArtifactLink(label="运行索引 manifest.json", href=manifest_path.as_uri())]
    if log_view.path is not None:
        artifact_links.append(ArtifactLink(label="本地日志", href=log_view.path.as_uri()))
    if wandb_view.local_path is not None:
        artifact_links.append(
            ArtifactLink(label="W&B 原始目录", href=wandb_view.local_path.as_uri())
        )
    artifact_links.append(
        ArtifactLink(
            label="Prometheus 实时查询",
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
        skills_used=_skills_for_manifest(manifest),
    )


def _skills_for_manifest(manifest: RunManifest) -> list[SkillUsage]:
    if manifest.formal_case:
        return [
            SkillUsage("01 customer-config", ".agents/skills/01-customer-config/SKILL.md", "读取客户配置、服务器和数据仓路径。"),
            SkillUsage("02 local-services-health", ".agents/skills/02-local-services/SKILL.md", "检查本地 W&B、Prometheus、Grafana 等服务。"),
            SkillUsage("03 server-hardware-probe", ".agents/skills/03-server-hardware/SKILL.md", "探测远程 NPU/内存/磁盘等硬件条件。"),
            SkillUsage("04 network-check", ".agents/skills/04-network-check/SKILL.md", "验证远程网络与代理可用性。"),
            SkillUsage("05 service-reachability", ".agents/skills/05-service-reachability/SKILL.md", "验证本地服务和远程服务互通。"),
            SkillUsage("06 train-stack-health", ".agents/skills/06-train-stack-health/SKILL.md", "验证训练栈、容器、依赖和最小运行条件。"),
            SkillUsage("07 data-collection", ".agents/skills/07-data-collection/SKILL.md", "采集日志、W&B、Prometheus evidence 和矩阵结果。"),
            SkillUsage("08 experiment-report", ".agents/skills/08-experiment-report/SKILL.md", "渲染本地报告并做交付件完整性检查。"),
            SkillUsage("verl adapter", "workspace-adapter/verl/SKILL.md", "沉淀 Verl GRPO 正式 case 的运行、命名、评测和诊断规则。"),
        ]
    return [
        SkillUsage("07 data-collection", ".agents/skills/07-data-collection/SKILL.md", "采集最小实验日志、W&B 和 Prometheus evidence。"),
        SkillUsage("08 experiment-report", ".agents/skills/08-experiment-report/SKILL.md", "渲染本地报告并做交付件完整性检查。"),
    ]
