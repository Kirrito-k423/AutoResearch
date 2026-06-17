"""Runtime bootstrap helpers for editable source checkouts."""
from __future__ import annotations

import sys
from pathlib import Path


def prefer_source_tree_adapters() -> None:
    """Keep local workspace layers ahead of stale wheel-copied packages."""
    repo_root = Path(__file__).resolve().parent.parent
    required_layers = ("workspace-core", "workspace-adapter", "datalake")
    if not all((repo_root / layer).exists() for layer in required_layers):
        return

    root_text = str(repo_root)
    sys.path[:] = [item for item in sys.path if item != root_text]
    sys.path.insert(0, root_text)
