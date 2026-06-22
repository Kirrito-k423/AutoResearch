"""Local log loading for experiment reports."""
from __future__ import annotations

from pathlib import Path

from datalake.manifest import RunManifest

from .models import LogView
from .paths import resolve_bundle_path


_KEY_PREFIXES = (
    "SUM=",
    "NPU_COUNT=",
    "WANDB_RUN_ID=",
    "wandb: Run summary:",
    "wandb: npu_count",
    "wandb:       sum",
    "wandb:       lib",
)


def load_log_view(
    manifest: RunManifest,
    tail_lines: int = 20,
    *,
    base_dir: Path | None = None,
) -> LogView:
    """Load key lines and a short tail excerpt from the local log."""
    if not manifest.log_files:
        return LogView(
            available=False,
            path=None,
            warning="manifest.log_files 为空，缺少本地日志产物。",
        )

    raw_path = manifest.log_files[0]
    path = resolve_bundle_path(
        raw_path,
        base_dir=base_dir or Path(manifest.workdir_local),
        run_id=manifest.run_id,
        alternates=[
            Path("3-raw-logs") / Path(raw_path).name,
            Path("logs") / Path(raw_path).name,
        ],
    )
    if path is None or not path.exists():
        return LogView(
            available=False,
            path=path,
            warning=f"日志文件不存在: {path}",
        )

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    key_lines = [
        line for line in lines
        if any(token in line for token in _KEY_PREFIXES)
    ]
    if not key_lines and lines:
        key_lines = lines[: min(5, len(lines))]
    return LogView(
        available=True,
        path=path,
        key_lines=key_lines,
        tail_lines=lines[-tail_lines:],
    )
