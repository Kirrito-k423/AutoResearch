"""Local wandb summary loading for experiment reports."""
from __future__ import annotations

import json
from pathlib import Path

from datalake.manifest import RunManifest

from .models import ArtifactLink, MetricPoint, WandbView


def load_wandb_view(
    manifest: RunManifest,
    *,
    base_url: str = "http://localhost:8080",
) -> WandbView:
    """Load a minimal local wandb summary for one run."""
    run_id = manifest.wandb_run_id
    local_path = manifest.wandb_path
    links = [ArtifactLink(label="W&B Local", href=base_url, note=run_id or "")]

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
    links.append(ArtifactLink(label="wandb artifact dir", href=path.as_uri()))
    summary_path = path / "files" / "wandb-summary.json"
    if not summary_path.exists():
        return WandbView(
            available=False,
            run_id=run_id,
            local_path=path,
            service_url=base_url,
            links=links,
            warning=f"缺少 wandb summary 文件: {summary_path}",
        )

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    step = float(summary.get("_step", 0) or 0)
    charts: dict[str, list[MetricPoint]] = {}
    for key in ("sum", "npu_count"):
        value = summary.get(key)
        if isinstance(value, (int, float)):
            charts[key] = [MetricPoint(x=step, y=float(value), label=f"step {int(step)}")]

    return WandbView(
        available=True,
        run_id=run_id,
        local_path=path,
        service_url=base_url,
        summary=summary,
        charts=charts,
        links=links,
    )
