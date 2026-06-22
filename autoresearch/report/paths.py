"""Path helpers for portable report bundles."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable


def resolve_bundle_path(
    value: object,
    *,
    base_dir: Path,
    run_id: str | None = None,
    alternates: Iterable[str | Path] = (),
) -> Path | None:
    """Resolve manifest paths that may still point at the original run root.

    Data bundles are copied into the log repository, while older manifests may
    contain absolute paths under ``~/.autoresearch/runs/<run_id>``. Prefer the
    recorded path when it still exists, then fall back to the copied bundle.
    """
    if value is None:
        return None
    base_dir = Path(base_dir)
    path = value if isinstance(value, Path) else Path(str(value)).expanduser()

    candidates: list[Path] = []
    if path.is_absolute():
        if run_id and run_id in path.parts:
            index = path.parts.index(run_id)
            rel_parts = path.parts[index + 1 :]
            if rel_parts:
                candidates.append(base_dir / Path(*rel_parts))
        candidates.append(base_dir / path.name)
    else:
        candidates.append(base_dir / path)

    for alternate in alternates:
        candidates.append(base_dir / Path(alternate))
    if path.is_absolute():
        candidates.append(path)
    elif path.exists():
        candidates.append(path)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if candidates else path
