"""Tests for editable checkout bootstrap behavior."""
from __future__ import annotations

import sys
from pathlib import Path

from autoresearch._bootstrap import prefer_source_tree_adapters


def test_prefer_source_tree_adapters_moves_repo_root_first(monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    original = ["/tmp/site-packages", str(repo_root), "/tmp/other"]
    monkeypatch.setattr(sys, "path", original.copy())

    prefer_source_tree_adapters()

    assert sys.path[0] == str(repo_root)
    assert sys.path.count(str(repo_root)) == 1
