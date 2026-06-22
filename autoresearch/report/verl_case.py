"""Formal Verl case report loading."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

from datalake.manifest import RunManifest

from .models import ArtifactStatus, VerlCaseMatrixRowView, VerlCaseView
from .paths import resolve_bundle_path


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
    config_payload = _load_config_payload(manifest, base_dir=base_dir)
    config = config_payload.get("config", {}) if isinstance(config_payload, dict) else {}
    trainer_val_only = bool(config.get("trainer_val_only", True)) if config else None

    matrix_path = _resolve_path(
        manifest.formal_case.get("matrix_results"),
        base_dir=base_dir,
        run_id=manifest.run_id,
        alternates=["matrix-results.jsonl"],
    )
    rows: list[VerlCaseMatrixRowView] = []
    if matrix_path and matrix_path.exists():
        rows = [_row_view(row) for row in _read_jsonl(matrix_path)]
    else:
        warnings.append("缺少 matrix-results.jsonl")

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
        trainer_val_only=trainer_val_only,
        training_mode=_training_mode_label(trainer_val_only),
        score_diagnostics=_score_diagnostics(rows, config=config, trainer_val_only=trainer_val_only),
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


def _resolve_path(
    value: Any,
    *,
    base_dir: Path,
    run_id: str | None,
    alternates: list[str | Path] | None = None,
) -> Path | None:
    return resolve_bundle_path(
        value,
        base_dir=base_dir,
        run_id=run_id,
        alternates=alternates or (),
    )


def _artifact_statuses(manifest: RunManifest, *, base_dir: Path) -> list[ArtifactStatus]:
    formal = manifest.formal_case or {}
    specs = [
        ("manifest", "运行索引", base_dir / "manifest.json", []),
        ("config", "不可变配置", manifest.config_snapshot, ["config.lock.json"]),
        ("provenance", "代码版本锁", base_dir / "provenance.json" if manifest.provenance else formal.get("provenance"), ["provenance.lock.json"]),
        ("matrix", "矩阵结果", formal.get("matrix_results"), ["matrix-results.jsonl"]),
        ("log", "日志", manifest.log_files[0] if manifest.log_files else formal.get("log_path"), [Path("logs") / "verl-case.log"]),
        ("wandb", "W&B 原始数据", manifest.wandb_path, ["wandb"]),
        ("prometheus", "Prometheus evidence", manifest.prom_metrics_file, [Path("prom") / "formal-case-prometheus.json"]),
    ]
    statuses = []
    for key, name, raw_path, alternates in specs:
        path = _normalize_path(raw_path, base_dir=base_dir, run_id=manifest.run_id, alternates=alternates)
        ok = bool(path and path.exists())
        statuses.append(
            ArtifactStatus(
                name=name,
                path=path,
                ok=ok,
                warning=None if ok else f"缺少交付件: {name}",
                key=key,
            )
        )
    return statuses


def _normalize_path(
    value: Any,
    *,
    base_dir: Path,
    run_id: str | None,
    alternates: list[str | Path] | None = None,
) -> Path | None:
    return resolve_bundle_path(
        value,
        base_dir=base_dir,
        run_id=run_id,
        alternates=alternates or (),
    )


def _expected_matrix(manifest: RunManifest, *, base_dir: Path) -> set[tuple[int, int, str]]:
    payload = _load_config_payload(manifest, base_dir=base_dir)
    try:
        config = payload.get("config", {})
        input_tokens = int(config.get("input_tokens") or 1024)
        outputs = [int(item) for item in config.get("output_tokens", [2048, 4096, 8192, 16384])]
        modes = [str(item) for item in config.get("inference_modes", ["sync", "async"])]
        return {(input_tokens, output, mode) for output in outputs for mode in modes}
    except (ValueError, TypeError, AttributeError):
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
        warnings.append(f"缺少或失败的矩阵行: {mode} {input_tokens}->{output_tokens}")
    return not missing


def _load_config_payload(manifest: RunManifest, *, base_dir: Path) -> dict[str, Any]:
    config_path = _resolve_path(
        manifest.config_snapshot,
        base_dir=base_dir,
        run_id=manifest.run_id,
        alternates=["config.lock.json"],
    )
    if config_path and config_path.exists():
        try:
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            return payload if isinstance(payload, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def _training_mode_label(trainer_val_only: bool | None) -> str:
    if trainer_val_only is True:
        return "验证矩阵: trainer.val_only=True，仅执行验证/推理，不更新模型参数。"
    if trainer_val_only is False:
        return "训练矩阵: trainer.val_only=False，会进入 GRPO 训练流程。"
    return "训练模式未知: 未找到 trainer_val_only 配置。"


def _score_diagnostics(
    rows: list[VerlCaseMatrixRowView],
    *,
    config: dict[str, Any],
    trainer_val_only: bool | None,
) -> list[str]:
    notes: list[str] = []
    if trainer_val_only is True:
        notes.append("当前配置是验证模式，0 分只说明基座模型在这批验证样本上的严格 acc/reward 为 0，不代表 GRPO 训练后效果。")
    if rows and all((row.accuracy == 0.0) for row in rows if row.accuracy is not None):
        notes.append("矩阵所有行 accuracy 都是 0；请优先查看 rows/*/validation/0.jsonl 中的 output/gts/acc 字段。")
        notes.append("历史样本中出现过模型算出数值但未按要求输出 \\boxed{} 的情况，verl/geo3k 的严格 reward 会记为 0。")
    val_max_samples = config.get("val_max_samples")
    if val_max_samples is not None:
        notes.append(f"本次每行验证样本上限 val_max_samples={val_max_samples}，样本量很小，适合穿刺性能链路，不适合下最终精度结论。")
    return notes


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
