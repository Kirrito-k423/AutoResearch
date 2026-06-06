"""autoresearch services status — 并发查 4 服务 healthz。

实现 SVC-CHK-STAT-01 (并发)、SVC-CHK-STAT-02 (字段)、
SVC-CHK-STAT-03 (--json 机读输出)。
"""
from __future__ import annotations

import json
import sys

from ._common import check_all, SERVICES


def _print_human(results: list, lang: str) -> None:
    """人读表格输出。"""
    name_w = max(len("NAME"), max(len(r["name"]) for r in results))
    url_w = max(len("URL"), max(len(r["url"]) for r in results))
    hdr = f"{'NAME':<{name_w}}  {'URL':<{url_w}}  {'HEALTHY':<8}  {'LATENCY_MS':<10}"
    print(hdr)
    for r in results:
        mark = "✓" if r["healthy"] else "✗"
        print(
            f"{r['name']:<{name_w}}  {r['url']:<{url_w}}  {mark:<8}  {r['latency_ms']:<10}"
        )


def _print_json(results: list) -> None:
    """机读 JSON 输出（最终 stdout 唯一 JSON 对象）。"""
    out = {
        "services": results,
        "summary": {
            "total": len(results),
            "healthy": sum(1 for r in results if r["healthy"]),
            "unhealthy": sum(1 for r in results if not r["healthy"]),
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def run_status(*, as_json: bool, lang: str) -> int:
    """Status 子命令主入口。

    Returns exit code: 0 = all healthy, 1 = any unhealthy, 2 = error.
    """
    try:
        results = check_all()
    except Exception as e:
        msg = f"错误：探测失败: {e}" if lang == "zh" else f"Error: probe failed: {e}"
        print(msg, file=sys.stderr)
        return 2

    if as_json:
        _print_json(results)
    else:
        _print_human(results, lang)
        n_h = sum(1 for r in results if r["healthy"])
        n_total = len(results)
        if lang == "zh":
            print(
                f"\n共 {n_total} 服务，健康 {n_h}/{n_total}",
                file=sys.stderr,
            )
        else:
            print(
                f"\n{n_total} services, {n_h}/{n_total} healthy",
                file=sys.stderr,
            )

    return 0 if all(r["healthy"] for r in results) else 1
