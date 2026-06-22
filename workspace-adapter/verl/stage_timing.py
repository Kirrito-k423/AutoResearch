"""Extract Verl GRPO stage timing evidence from W&B and logs."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Literal

from pydantic import BaseModel


TimingSource = Literal["wandb", "log"]


class VerlStageTiming(BaseModel):
    """One normalized stage timing observation for a Verl case."""

    run_id: str
    case_id: str
    stage: str
    original_key: str
    elapsed_seconds: float
    source: TimingSource
    step: int | None = None
    raw_line: str | None = None


def normalize_stage_metric_key(key: str) -> str:
    """Map verbose Verl/W&B timing metric names into stable report stages."""
    lowered = _normalize_key(key)
    if "ref" in lowered and ("logprob" in lowered or "logp" in lowered or "log_prob" in lowered):
        return "ref_logp"
    if "rollout" in lowered or "generate" in lowered or "inference" in lowered:
        return "rollout"
    if "logprob" in lowered or "logp" in lowered or "log_prob" in lowered:
        return "logp"
    if "reward" in lowered or "score" in lowered:
        return "reward"
    if "advantage" in lowered or "gae" in lowered:
        return "advantage"
    if any(token in lowered for token in ("update", "backward", "optimizer", "optim", "actor_update")):
        return "update"
    if "validation" in lowered or re.search(r"(^|_)val(_|$)", lowered):
        return "validation"
    if "checkpoint" in lowered or "save" in lowered:
        return "checkpointing"
    if "dataloader" in lowered or "data_load" in lowered or "load_data" in lowered:
        return "data_loading"
    return "other"


def extract_stage_timings_from_wandb_run(
    run_dir: str | Path,
    *,
    run_id: str,
    case_id: str,
) -> list[VerlStageTiming]:
    """Extract timing-like W&B summary/history keys from a local offline run dir."""
    root = Path(run_dir)
    if not root.exists():
        return []

    timings: list[VerlStageTiming] = []
    for path in _candidate_wandb_json_files(root):
        for record, raw_line in _iter_json_records(path):
            step = _step_from_record(record)
            for key, value in _flatten_record(record):
                elapsed = _elapsed_seconds(key, value)
                if elapsed is None:
                    continue
                timings.append(
                    VerlStageTiming(
                        run_id=run_id,
                        case_id=case_id,
                        stage=normalize_stage_metric_key(key),
                        original_key=key,
                        elapsed_seconds=elapsed,
                        source="wandb",
                        step=step,
                        raw_line=raw_line,
                    )
                )
    return _dedupe_timings(timings)


def _candidate_wandb_json_files(root: Path) -> list[Path]:
    names = (
        "wandb-history.jsonl",
        "wandb-history.json",
        "wandb-summary.json",
        "history.jsonl",
        "summary.json",
    )
    paths: list[Path] = []
    for name in names:
        paths.extend(sorted(root.glob(f"**/{name}")))
    return paths


def _iter_json_records(path: Path) -> Iterable[tuple[dict[str, Any], str | None]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    if path.suffix == ".jsonl":
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                yield payload, stripped
        return
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return
    if isinstance(payload, dict):
        yield payload, None
    elif isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item, json.dumps(item, ensure_ascii=False)


def _flatten_record(record: dict[str, Any], prefix: str = "") -> Iterable[tuple[str, Any]]:
    for key, value in record.items():
        full_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            yield from _flatten_record(value, full_key)
        else:
            yield full_key, value


def _elapsed_seconds(key: str, value: Any) -> float | None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    if not _looks_like_timing_key(key):
        return None
    elapsed = float(value)
    normalized = _normalize_key(key)
    if re.search(r"(^|_)ms(_|$)", normalized) or "millisecond" in normalized:
        elapsed = elapsed / 1000.0
    elif re.search(r"(^|_)min(_|$)", normalized):
        elapsed = elapsed * 60.0
    if elapsed < 0:
        return None
    return elapsed


def _looks_like_timing_key(key: str) -> bool:
    normalized = _normalize_key(key)
    if any(token in normalized for token in ("per_second", "per_sec", "throughput", "_rate")):
        return False
    timing_tokens = ("time", "timing", "latency", "duration", "elapsed", "seconds", "_sec", "_ms")
    if any(token in normalized for token in timing_tokens):
        return True
    return normalized.startswith("timer_") or normalized.startswith("timers_")


def _step_from_record(record: dict[str, Any]) -> int | None:
    for key in ("_step", "global_step", "trainer/global_step", "step"):
        value = record.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
    return None


def _normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def _dedupe_timings(rows: Iterable[VerlStageTiming]) -> list[VerlStageTiming]:
    seen: set[tuple[str, str, int | None, str, str]] = set()
    deduped: list[VerlStageTiming] = []
    for row in rows:
        key = (row.case_id, row.stage, row.step, row.original_key, row.source)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped
