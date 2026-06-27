#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {
    ".cfg",
    ".html",
    ".json",
    ".jsonl",
    ".log",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
}
SYSTEM_SUMMARY_KEYS = {"_runtime", "_timestamp", "_step", "_wandb"}
SUMMARY_METRIC_KEYS = {
    "accuracy",
    "consistency",
    "failed_rows",
    "lib",
    "latency_ms",
    "matrix_rows",
    "npu_count",
    "passed_rows",
    "sample_count",
    "sum",
    "tokens_per_second",
}
POSITIVE_PATTERNS = [
    re.compile(r"\bstep\s*:\s*\d+\s*-"),
    re.compile(r"Initial validation metrics"),
    re.compile(r"validation generation end"),
    re.compile(r"val-(?:core|aux)/"),
    re.compile(r"trainer/global_step"),
    re.compile(r'"(?:passed_rows|matrix_rows|sample_count)"\s*:\s*[1-9]'),
]


@dataclass
class UnitReport:
    path: str
    kind: str
    bytes: int
    files: int
    has_signal: bool
    signals: list[str]
    delete_candidate: bool
    selected_for_delete: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or delete W&B units that lack successful step evidence."
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Root to scan. Can be repeated. Defaults to common AutoResearch W&B roots.",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete selected no-signal W&B units. Omit for dry-run.",
    )
    parser.add_argument(
        "--prune-empty-dirs",
        action="store_true",
        help="After --delete, remove empty directories below each root.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit full JSON instead of a compact text report.",
    )
    return parser.parse_args()


def default_roots() -> list[Path]:
    home = Path.home()
    return [
        home / ".autoresearch" / "runs",
        home / "autoResearchData" / "autoresearch-log" / "wandb" / "offline-runs",
    ]


def is_unit(path: Path) -> bool:
    return path.is_dir() and (path.name == "wandb" or path.name.startswith("offline-run-"))


def discover_units(roots: list[Path]) -> list[Path]:
    units: set[Path] = set()
    for root in roots:
        root = root.expanduser().resolve()
        if not root.exists():
            continue
        if is_unit(root):
            units.add(root)
        for path in root.rglob("*"):
            if is_unit(path):
                units.add(path)
    return sorted(units, key=lambda p: (len(p.parts), str(p)))


def dir_size_and_file_count(path: Path) -> tuple[int, int]:
    total = 0
    count = 0
    for item in path.rglob("*"):
        if not item.is_file():
            continue
        count += 1
        try:
            total += item.stat().st_size
        except OSError:
            pass
    return total, count


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def summary_metric_signal(path: Path, unit: Path) -> str | None:
    try:
        data = json.loads(path.read_text(errors="ignore"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None

    for key, value in data.items():
        if key in SYSTEM_SUMMARY_KEYS:
            continue
        if key.startswith("val-core/") or key.startswith("val-aux/"):
            return f"{path.relative_to(unit)}::{key}"
        if key in SUMMARY_METRIC_KEYS and value not in (None, "", 0):
            return f"{path.relative_to(unit)}::{key}"

    metric_keys = [key for key in data if key not in SYSTEM_SUMMARY_KEYS and not key.startswith("_")]
    if metric_keys:
        return f"{path.relative_to(unit)}::{metric_keys[0]}"
    return None


def text_signal(path: Path, unit: Path) -> str | None:
    try:
        with path.open("r", errors="ignore") as handle:
            for line in handle:
                for pattern in POSITIVE_PATTERNS:
                    if pattern.search(line):
                        return f"{path.relative_to(unit)}::{pattern.pattern}"
    except OSError:
        return None
    return None


def collect_signals(unit: Path) -> list[str]:
    signals: list[str] = []
    for path in unit.rglob("*"):
        if not path.is_file():
            continue
        signal: str | None = None
        if path.name == "wandb-summary.json":
            signal = summary_metric_signal(path, unit)
        if signal is None and (path.suffix in TEXT_SUFFIXES or path.name == "output.log"):
            signal = text_signal(path, unit)
        if signal is not None:
            signals.append(signal)
    return signals


def build_reports(units: list[Path]) -> list[UnitReport]:
    reports: list[UnitReport] = []
    for unit in units:
        size, files = dir_size_and_file_count(unit)
        signals = collect_signals(unit)
        reports.append(
            UnitReport(
                path=str(unit),
                kind="offline-run" if unit.name.startswith("offline-run-") else "wandb-dir",
                bytes=size,
                files=files,
                has_signal=bool(signals),
                signals=signals[:8],
                delete_candidate=not bool(signals),
            )
        )
    return reports


def select_delete_paths(reports: list[UnitReport]) -> list[Path]:
    selected: list[Path] = []
    for report in reports:
        if not report.delete_candidate:
            continue
        path = Path(report.path)
        if any(is_relative_to(path, parent) for parent in selected):
            continue
        selected.append(path)
        report.selected_for_delete = True
    return selected


def prune_empty_dirs(roots: list[Path]) -> list[str]:
    pruned: list[str] = []
    for root in roots:
        root = root.expanduser().resolve()
        if not root.exists() or not root.is_dir():
            continue
        directories = sorted(
            (path for path in root.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        )
        for path in directories:
            try:
                path.rmdir()
            except OSError:
                continue
            pruned.append(str(path))
    return pruned


def print_text(
    reports: list[UnitReport],
    selected: list[Path],
    deleted: list[str],
    pruned: list[str],
    dry_run: bool,
) -> None:
    total = len(reports)
    kept = sum(1 for report in reports if report.has_signal)
    candidates = sum(1 for report in reports if report.delete_candidate)
    selected_bytes = sum(report.bytes for report in reports if report.selected_for_delete)
    mode = "DRY-RUN" if dry_run else "DELETE"
    print(f"{mode}: scanned={total} kept_with_signal={kept} candidates={candidates} selected={len(selected)} bytes={selected_bytes}")
    for report in reports:
        if not report.selected_for_delete:
            continue
        print(f"DELETE {report.bytes} bytes {report.files} files {report.path}")
    if deleted:
        print("deleted:")
        for path in deleted:
            print(path)
    if pruned:
        print("pruned_empty_dirs:")
        for path in pruned:
            print(path)


def main() -> int:
    args = parse_args()
    roots = args.root or default_roots()
    units = discover_units(roots)
    reports = build_reports(units)
    selected = select_delete_paths(reports)
    deleted: list[str] = []

    if args.delete:
        for path in selected:
            if path.exists():
                shutil.rmtree(path)
                deleted.append(str(path))
    pruned = prune_empty_dirs(roots) if args.delete and args.prune_empty_dirs else []

    payload = {
        "mode": "delete" if args.delete else "dry-run",
        "roots": [str(root.expanduser()) for root in roots],
        "scanned": len(reports),
        "kept_with_signal": sum(1 for report in reports if report.has_signal),
        "candidates": sum(1 for report in reports if report.delete_candidate),
        "selected_for_delete": [str(path) for path in selected],
        "deleted": deleted,
        "pruned_empty_dirs": pruned,
        "reports": [report.__dict__ for report in reports],
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text(reports, selected, deleted, pruned, dry_run=not args.delete)
    return 0


if __name__ == "__main__":
    sys.exit(main())
