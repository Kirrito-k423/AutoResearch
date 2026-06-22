"""Local Prometheus loading for experiment reports."""
from __future__ import annotations

import json
from pathlib import Path
from datetime import timedelta
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode, quote
from urllib.request import urlopen

from datalake.manifest import RunManifest

from .models import MetricPoint, PrometheusView
from .paths import resolve_bundle_path


METRIC_NAME = "autoresearch_npu_count"


def build_prom_query(run_id: str) -> str:
    """Build the stable per-run Prometheus query."""
    return f'{METRIC_NAME}{{run_id="{run_id}"}}'


def build_prom_query_url(run_id: str, *, base_url: str = "http://localhost:9090") -> str:
    """Build a browser-friendly Prometheus graph URL."""
    query = build_prom_query(run_id)
    return f"{base_url.rstrip('/')}/graph?g0.expr={quote(query, safe='')}&g0.tab=1"


def _read_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=2.0) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _matrix_url(manifest: RunManifest, base_url: str) -> str:
    start = manifest.started_at
    end = manifest.finished_at or (start + timedelta(seconds=1))
    if end <= start:
        end = start + timedelta(seconds=1)
    params = urlencode(
        {
            "query": build_prom_query(manifest.run_id),
            "start": start.timestamp(),
            "end": end.timestamp(),
            "step": 1,
        }
    )
    return f"{base_url.rstrip('/')}/api/v1/query_range?{params}"


def _instant_url(run_id: str, base_url: str) -> str:
    params = urlencode({"query": build_prom_query(run_id)})
    return f"{base_url.rstrip('/')}/api/v1/query?{params}"


def load_prometheus_view(
    manifest: RunManifest,
    *,
    base_url: str = "http://localhost:9090",
    base_dir: Path | None = None,
) -> PrometheusView:
    """Load local Prometheus data without making the report depend on it."""
    query = build_prom_query(manifest.run_id)
    query_url = build_prom_query_url(manifest.run_id, base_url=base_url)
    evidence_path, evidence = _load_evidence(manifest, base_dir=base_dir)
    notes = _evidence_notes(evidence)
    default = PrometheusView(
        available=False,
        metric_name=METRIC_NAME,
        query=query,
        query_url=query_url,
        service_url=base_url,
        current_value=None,
        series=[],
        evidence_path=evidence_path,
        notes=notes,
        warning=None,
    )

    try:
        matrix = _read_json(_matrix_url(manifest, base_url))
        results = matrix.get("data", {}).get("result", [])
        if results:
            values = results[0].get("values", [])
            series = [
                MetricPoint(x=float(ts), y=float(value), label="")
                for ts, value in values
            ]
            current_value = series[-1].y if series else None
            default.available = True
            default.series = series
            default.current_value = current_value
            return default
    except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        pass

    try:
        instant = _read_json(_instant_url(manifest.run_id, base_url))
        results = instant.get("data", {}).get("result", [])
        if results:
            value = results[0].get("value")
            if isinstance(value, list) and len(value) == 2:
                point = MetricPoint(x=float(value[0]), y=float(value[1]), label="instant")
                default.available = True
                default.series = [point]
                default.current_value = point.y
                return default
        default.warning = "Prometheus 查询成功但未返回该 run 的实时指标；请优先查看本地 evidence。"
        return default
    except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        default.warning = f"Prometheus 不可达或返回异常: {exc}"
        return default


def _load_evidence(
    manifest: RunManifest,
    *,
    base_dir: Path | None,
) -> tuple[Path | None, dict[str, Any]]:
    path = resolve_bundle_path(
        manifest.prom_metrics_file,
        base_dir=base_dir or Path(manifest.workdir_local),
        run_id=manifest.run_id,
        alternates=[Path("prom") / "formal-case-prometheus.json"],
    )
    if path is None or not path.exists():
        return path, {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return path, {}
    return path, payload if isinstance(payload, dict) else {}


def _evidence_notes(evidence: dict[str, Any]) -> list[str]:
    if not evidence:
        return []
    notes: list[str] = []
    if "npu_count" in evidence:
        notes.append(f"本地 evidence 记录 NPU 数量: {evidence['npu_count']}")
    metrics = evidence.get("metrics_pushed")
    if isinstance(metrics, list) and metrics:
        notes.append("已推送指标: " + ", ".join(str(item) for item in metrics))
    missing = evidence.get("missing_resource_metrics")
    if isinstance(missing, list) and missing:
        notes.append("尚未采集资源指标: " + ", ".join(str(item) for item in missing))
    if not metrics and not any(
        key in evidence
        for key in (
            "autoresearch_npu_hbm_used_mib",
            "autoresearch_npu_hbm_total_mib",
            "autoresearch_npu_aicore_utilization_percent",
        )
    ):
        notes.append("当前 evidence 只证明 run 级别 NPU 数量，不包含 HBM 显存或 AI Core 利用率曲线。")
    note = evidence.get("note")
    if isinstance(note, str) and note:
        notes.append(note)
    return notes
