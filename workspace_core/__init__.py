"""Development import shim for the ``workspace-core`` source tree.

The wheel maps ``workspace-core`` to ``workspace_core`` via hatch
``force-include``. Editable installs do not apply that mapping, so local
tests need this package path extension to import the source tree directly.
"""
from __future__ import annotations

from pathlib import Path

_SOURCE = Path(__file__).resolve().parent.parent / "workspace-core"
if _SOURCE.exists():
    __path__.append(str(_SOURCE))  # type: ignore[name-defined]
