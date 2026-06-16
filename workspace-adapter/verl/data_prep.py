"""geometry3k preparation boundary for the formal Verl case."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .case_config import VerlCaseConfig


class DataPrepError(Exception):
    """Raised when a geometry3k row cannot be preserved for multimodal use."""


class PreparedGeometry3K(BaseModel):
    """Prepared local dataset paths."""

    dataset_id: str
    cache_root: Path
    model_cache: Path
    dataset_cache: Path
    image_dir: Path
    jsonl_path: Path
    sample_count: int
    ready: bool


def _load_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("train", "data", "rows", "samples"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    raise DataPrepError(f"unsupported geometry3k fixture shape: {path}")


def _pick(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return value
    return None


def _normalize_row(row: dict[str, Any], index: int) -> dict[str, Any]:
    image = _pick(row, "image", "image_path", "img", "diagram")
    problem = _pick(row, "problem", "prompt", "question", "text")
    answer = _pick(row, "answer", "label", "solution", "ground_truth")
    if image is None:
        raise DataPrepError(f"geometry3k row {index} missing image")
    if problem is None:
        raise DataPrepError(f"geometry3k row {index} missing problem")
    if answer is None:
        raise DataPrepError(f"geometry3k row {index} missing answer")
    return {
        "sample_id": str(row.get("id") or row.get("sample_id") or index),
        "image": str(image),
        "problem": str(problem),
        "answer": str(answer),
    }


def prepare_geometry3k(
    config: VerlCaseConfig,
    cache_root: str | Path,
    *,
    max_samples: int | None = None,
    local_dataset_path: str | Path | None = None,
) -> PreparedGeometry3K:
    """Prepare a Verl-ready geometry3k JSONL file without silent text fallback."""
    root = Path(cache_root).expanduser()
    model_cache = root / "models" / config.model_id.replace("/", "__")
    dataset_cache = root / "datasets" / config.dataset_id.replace("/", "__")
    image_dir = dataset_cache / "images"
    jsonl_path = dataset_cache / "geometry3k-verl.jsonl"
    for path in (model_cache, dataset_cache, image_dir):
        path.mkdir(parents=True, exist_ok=True)

    if local_dataset_path is None:
        return PreparedGeometry3K(
            dataset_id=config.dataset_id,
            cache_root=root,
            model_cache=model_cache,
            dataset_cache=dataset_cache,
            image_dir=image_dir,
            jsonl_path=jsonl_path,
            sample_count=0,
            ready=jsonl_path.exists(),
        )

    rows = _load_rows(Path(local_dataset_path).expanduser())
    if max_samples is not None:
        rows = rows[:max_samples]
    normalized = [_normalize_row(row, idx) for idx, row in enumerate(rows)]
    jsonl_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in normalized),
        encoding="utf-8",
    )
    return PreparedGeometry3K(
        dataset_id=config.dataset_id,
        cache_root=root,
        model_cache=model_cache,
        dataset_cache=dataset_cache,
        image_dir=image_dir,
        jsonl_path=jsonl_path,
        sample_count=len(normalized),
        ready=True,
    )
