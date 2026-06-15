"""Persist run manifests under ``~/.autoresearch/runs``."""
from __future__ import annotations

import json
from pathlib import Path

from .schema import RunManifest


DEFAULT_RUNS_ROOT = Path("~/.autoresearch/runs").expanduser()


def write(m: RunManifest, root: Path = DEFAULT_RUNS_ROOT) -> Path:
    """Write ``manifest.json`` for a run and return its path."""
    run_dir = Path(root).expanduser() / m.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "manifest.json"
    payload = m.model_dump(mode="json")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
