"""Local wandb summary loading for experiment reports."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from statistics import mean
from typing import Any

from datalake.manifest import RunManifest

from .models import ArtifactLink, MetricPoint, WandbView
from .paths import resolve_bundle_path


stage_timing_mod = importlib.import_module("workspace-adapter.verl.stage_timing")
extract_stage_timings_from_wandb_run = stage_timing_mod.extract_stage_timings_from_wandb_run


def load_wandb_view(
    manifest: RunManifest,
    *,
    base_url: str = "http://localhost:8080",
    base_dir: Path | None = None,
) -> WandbView:
    """Load a minimal local wandb summary for one run."""
    run_id = manifest.wandb_run_id
    bundle_dir = base_dir or Path(manifest.workdir_local)
    local_path = resolve_bundle_path(
        manifest.wandb_path,
        base_dir=bundle_dir,
        run_id=manifest.run_id,
        alternates=["1-wandb", "wandb"],
    )
    links = [ArtifactLink(label="W&B 本地首页", href=base_url, note=run_id or "")]

    if local_path is None:
        return WandbView(
            available=False,
            run_id=run_id,
            local_path=None,
            service_url=base_url,
            links=links,
            warning="manifest 未记录 wandb_path。",
        )

    path = Path(local_path)
    links.append(ArtifactLink(label="W&B 原始目录", href=path.as_uri()))
    run_links = _load_run_links(path)
    links.extend(run_links[:8])
    summary_path = path / "files" / "wandb-summary.json"
    if not summary_path.exists():
        summary = _summary_from_matrix(bundle_dir)
        stage_timings = _load_stage_timings(path, manifest)
        if summary:
            summary = _with_stage_timing_summary(summary, stage_timings)
            charts = {
                **_charts_from_summary(summary),
                **_charts_from_stage_timings(stage_timings),
            }
            return WandbView(
                available=True,
                run_id=run_id,
                local_path=path,
                service_url=base_url,
                summary=summary,
                charts=charts,
                links=links,
                run_links=run_links,
                warning=(
                    "缺少 wandb-summary.json，报告已用 matrix-results.jsonl 生成汇总；"
                    "W&B Web 历史视图请用 1-wandb/rebuild-wandb.sh 或全局 rebuild-all.sh 恢复。"
                ),
            )
        if stage_timings:
            summary = _with_stage_timing_summary({}, stage_timings)
            return WandbView(
                available=True,
                run_id=run_id,
                local_path=path,
                service_url=base_url,
                summary=summary,
                charts=_charts_from_stage_timings(stage_timings),
                links=links,
                run_links=run_links,
                warning=(
                    "缺少 wandb-summary.json，但已从 W&B history/summary 文件提取 Verl stage timing。"
                ),
            )
        return WandbView(
            available=bool(run_links),
            run_id=run_id,
            local_path=path,
            service_url=base_url,
            links=links,
            run_links=run_links,
            warning=f"缺少 wandb summary 文件: {summary_path}",
        )

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    stage_timings = _load_stage_timings(path, manifest)
    summary = _with_stage_timing_summary(summary, stage_timings)
    return WandbView(
        available=True,
        run_id=run_id,
        local_path=path,
        service_url=base_url,
        summary=summary,
        charts={
            **_charts_from_summary(summary),
            **_charts_from_stage_timings(stage_timings),
        },
        links=links,
        run_links=run_links,
    )


def _load_run_links(wandb_path: Path) -> list[ArtifactLink]:
    runs_path = wandb_path / "runs.json"
    if not runs_path.exists():
        return []
    try:
        rows = json.loads(runs_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    links: list[ArtifactLink] = []
    if not isinstance(rows, list):
        return links
    for row in rows:
        if not isinstance(row, dict):
            continue
        url = str(row.get("local_url") or "").strip()
        name = str(row.get("display_name") or row.get("wandb_run_id") or "").strip()
        if url and name:
            links.append(ArtifactLink(label=name, href=url, note=str(row.get("project") or "")))
    return links


def _summary_from_matrix(bundle_dir: Path) -> dict[str, Any]:
    matrix_path = next(
        (
            path for path in (
                bundle_dir / "6-rows" / "matrix-results.jsonl",
                bundle_dir / "matrix-results.jsonl",
            )
            if path.exists()
        ),
        bundle_dir / "matrix-results.jsonl",
    )
    if not matrix_path.exists():
        return {}
    rows = []
    for line in matrix_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    if not rows:
        return {}

    def avg(key: str) -> float | None:
        values = [float(row[key]) for row in rows if isinstance(row.get(key), (int, float))]
        return float(mean(values)) if values else None

    passed = [row for row in rows if row.get("status") == "passed"]
    return {
        "summary_source": "matrix-results.jsonl",
        "matrix_rows": len(rows),
        "passed_rows": len(passed),
        "failed_rows": len(rows) - len(passed),
        "sample_count": sum(int(row.get("sample_count") or 0) for row in rows),
        "tokens_per_second": avg("tokens_per_second"),
        "latency_ms": avg("latency_ms"),
        "accuracy": avg("accuracy"),
        "consistency": avg("consistency"),
        "_step": len(rows),
    }


def _charts_from_summary(summary: dict[str, Any]) -> dict[str, list[MetricPoint]]:
    step = float(summary.get("_step", 0) or 0)
    charts: dict[str, list[MetricPoint]] = {}
    for key in ("sum", "npu_count", "tokens_per_second", "accuracy", "consistency"):
        value = summary.get(key)
        if isinstance(value, (int, float)):
            charts[key] = [MetricPoint(x=step, y=float(value), label=f"step {int(step)}")]
    return charts


def _load_stage_timings(wandb_path: Path, manifest: RunManifest) -> list[Any]:
    return extract_stage_timings_from_wandb_run(
        wandb_path,
        run_id=manifest.run_id,
        case_id=manifest.run_id,
    )


def _with_stage_timing_summary(summary: dict[str, Any], timings: list[Any]) -> dict[str, Any]:
    if not timings:
        return summary
    stages = sorted({str(row.stage) for row in timings})
    return {
        **summary,
        "stage_timing_rows": len(timings),
        "stage_timing_stages": ", ".join(stages),
        "stage_timing_total_seconds": sum(float(row.elapsed_seconds) for row in timings),
    }


def _charts_from_stage_timings(timings: list[Any]) -> dict[str, list[MetricPoint]]:
    charts: dict[str, list[MetricPoint]] = {}
    for index, row in enumerate(timings):
        step = row.step if isinstance(row.step, int) else index
        key = f"stage_timing/{row.stage}"
        charts.setdefault(key, []).append(
            MetricPoint(
                x=float(step),
                y=float(row.elapsed_seconds),
                label=str(row.original_key),
            )
        )
    return charts
