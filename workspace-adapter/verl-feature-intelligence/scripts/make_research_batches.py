#!/usr/bin/env python3
"""Create subagent research batch files from needs-research.txt."""

from __future__ import annotations

import argparse
from pathlib import Path


def read_items(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="从 needs-research.txt 生成子代理补证批次。")
    parser.add_argument("--needs", default="docs/verl/features/process/needs-research.txt", help="待补参数清单")
    parser.add_argument("--out", default="docs/verl/features/process/batches", help="批次输出目录")
    parser.add_argument("--start", type=int, required=True, help="起始 batch 编号，例如 13")
    parser.add_argument("--count", type=int, default=6, help="生成多少个批次")
    parser.add_argument("--batch-size", type=int, default=30, help="每批参数数")
    args = parser.parse_args()

    needs_path = Path(args.needs).expanduser()
    out_dir = Path(args.out).expanduser()
    if not needs_path.is_absolute():
        needs_path = Path.cwd() / needs_path
    if not out_dir.is_absolute():
        out_dir = Path.cwd() / out_dir

    items = read_items(needs_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for offset in range(args.count):
        start = offset * args.batch_size
        chunk = items[start : start + args.batch_size]
        if not chunk:
            break
        batch_no = args.start + offset
        path = out_dir / f"batch-{batch_no:02d}.txt"
        path.write_text("\n".join(chunk) + "\n")
        print(f"{path}\t{len(chunk)}")
        written += 1
    print(f"written_batches\t{written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
