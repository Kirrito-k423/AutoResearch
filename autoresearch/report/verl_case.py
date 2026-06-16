"""Formal Verl case report loading."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

from datalake.manifest import RunManifest

from .models import ArtifactStatus, VerlCaseMatrixRowView, VerlCaseView


def load_verl_case_view(
    manifest: RunManifest,
    *,
    manifest_path: Path | None = None,
) -> VerlCaseView | None:
    """Load and summarize formal Verl case matrix artifacts."""
    if not manifest.formal_case:
        return None

    base_dir = manifest_path.parent if manifest_path else Path(manifest.workdir_local)
    warnings: list[str] = []
    artifacts = _artifact_statuses(manifest, base_dir=base_dir)
    warnings.extend(item.warning for item in artifacts if item.warning)

    matrix_path = _resolve_path(manifest.formal_case.get("matrix_results"), base_dir=base_dir)
    rows: list[VerlCaseMatrixRowView] = []
    if matrix_path and matrix_path.exists():
        rows = [_row_view(row) for row in _read_jsonl(matrix_path)]
    else:
        warnings.append("matrix-results.jsonl missing")

    expected = _expected_matrix(manifest, base_dir=base_dir)
    complete_matrix = _complete_matrix(rows, expected, warnings)
    return VerlCaseView(
        available=True,
        complete_matrix=complete_matrix,
        rows=rows,
        length_summary=_length_summary(rows),
        mode_summary=_mode_summary(rows),
        async_comparison=_async_comparison(rows),
        accuracy_overall=_avg([row.accuracy for row in rows]),
        consistency_overall=_avg([row.consistency for row in rows]),
        artifacts=artifacts,
        warnings=warnings,
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _row_view(row: dict[str, Any]) -> VerlCaseMatrixRowView:
    return VerlCaseMatrixRowView(
        input_tokens=int(row.get("input_tokens") or 0),
        output_tokens=int(row.get("output_tokens") or 0),
        mode=str(row.get("inference_mode") or row.get("mode") or ""),
        status=str(row.get("status") or "failed"),
        tokens_per_second=_num(row.get("tokens_per_second")),
        latency_ms=_num(row.get("latency_ms")),
        sample_count=int(row.get("sample_count") or 0),
        accuracy=_num(row.get("accuracy")),
        consistency=_num(row.get("consistency")),
        error=row.get("error"),
    )


def _resolve_path(value: Any, *, base_dir: Path) -> Path | None:
    if not value:
        return None
    path = Path(str(value)).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path


def _artifact_statuses(manifest: RunManifest, *, base_dir: Path) -> list[ArtifactStatus]:
    formal = manifest.formal_case or {}
    specs = [
        ("manifest", base_dir / "manifest.json"),
        ("config snapshot", manifest.config_snapshot),
        ("provenance", base_dir / "provenance.json" if manifest.provenance else formal.get("provenance")),
        ("matrix results", formal.get("matrix_results")),
        ("log", manifest.log_files[0] if manifest.log_files else formal.get("log_path")),
        ("wandb", manifest.wandb_path),
        ("prometheus evidence", manifest.prom_metrics_file),
    ]
    statuses = []
    for name, raw_path in specs:
        path = _normalize_path(raw_path, base_dir=base_dir)
        ok = bool(path and path.exists())
        statuses.append(
            ArtifactStatus(
                name=name,
                path=path,
                ok=ok,
                warning=None if ok else f"missing artifact: {name}",
            )
        )
    return statuses


def _normalize_path(value: Any, *, base_dir: Path) -> Path | None:
    if value is None:
        return None
    path = value if isinstance(value, Path) else Path(str(value)).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path


def _expected_matrix(manifest: RunManifest, *, base_dir: Path) -> set[tuple[int, int, str]]:
    config_path = _resolve_path(manifest.config_snapshot, base_dir=base_dir)
    if config_path and config_path.exists():
        try:
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            config = payload.get("config", {})
            input_tokens = int(config.get("input_tokens") or 1024)
            outputs = [int(item) for item in config.get("output_tokens", [2048, 4096, 8192, 16384])]
            modes = [str(item) for item in config.get("inference_modes", ["sync", "async"])]
            return {(input_tokens, output, mode) for output in outputs for mode in modes}
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
    return {(1024, output, mode) for output in (2048, 4096, 8192, 16384) for mode in ("sync", "async")}


def _complete_matrix(
    rows: list[VerlCaseMatrixRowView],
    expected: set[tuple[int, int, str]],
    warnings: list[str],
) -> bool:
    passed = {
        (row.input_tokens, row.output_tokens, row.mode)
        for row in rows
        if row.status == "passed"
    }
    missing = sorted(expected - passed)
    for input_tokens, output_tokens, mode in missing:
        warnings.append(f"missing or failed matrix row: {mode} {input_tokens}->{output_tokens}")
    return not missing


def _length_summary(rows: list[VerlCaseMatrixRowView]) -> list[dict[str, Any]]:
    summary = []
    for output_tokens in sorted({row.output_tokens for row in rows}):
        chunk = [row for row in rows if row.output_tokens == output_tokens]
        summary.append(
            {
                "output_tokens": output_tokens,
                "success_rate": _success_rate(chunk),
                "tokens_per_second": _avg([row.tokens_per_second for row in chunk]),
                "latency_ms": _avg([row.latency_ms for row in chunk]),
            }
        )
    return summary


def _mode_summary(rows: list[VerlCaseMatrixRowView]) -> list[dict[str, Any]]:
    summary = []
    for mode in sorted({row.mode for row in rows}):
        chunk = [row for row in rows if row.mode == mode]
        summary.append(
            {
                "mode": mode,
                "success_rate": _success_rate(chunk),
                "accuracy": _avg([row.accuracy for row in chunk]),
                "tokens_per_second": _avg([row.tokens_per_second for row in chunk]),
                "latency_ms": _avg([row.latency_ms for row in chunk]),
            }
        )
    return summary


def _async_comparison(rows: list[VerlCaseMatrixRowView]) -> list[dict[str, Any]]:
    output_tokens = sorted({row.output_tokens for row in rows})
    comparisons = []
    for output in output_tokens:
        sync = next((row for row in rows if row.output_tokens == output and row.mode == "sync"), None)
        async_row = next((row for row in rows if row.output_tokens == output and row.mode == "async"), None)
        if not sync or not async_row:
            continue
        comparisons.append(
            {
                "output_tokens": output,
                "tokens_per_second_delta": _delta(async_row.tokens_per_second, sync.tokens_per_second),
                "latency_ms_delta": _delta(async_row.latency_ms, sync.latency_ms),
                "accuracy_delta": _delta(async_row.accuracy, sync.accuracy),
                "consistency_delta": _delta(async_row.consistency, sync.consistency),
            }
        )
    return comparisons


def _success_rate(rows: list[VerlCaseMatrixRowView]) -> float | None:
    if not rows:
        return None
    return sum(1 for row in rows if row.status == "passed") / len(rows)


def _avg(values: list[float | None]) -> float | None:
    numeric = [value for value in values if value is not None]
    if not numeric:
        return None
    return float(mean(numeric))


def _delta(value: float | None, baseline: float | None) -> float | None:
    if value is None or baseline is None:
        return None
    return value - baseline


def _num(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
