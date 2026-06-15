"""CLI for rendering local experiment reports."""
from __future__ import annotations

import json
import webbrowser
from pathlib import Path
from typing import Any

import click

from .loader import load_report_bundle
from .render import render_report


def run_render(
    *,
    run_id: str,
    open_report: bool = False,
    runs_root: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    """Render one local HTML report and optionally open it."""
    bundle = load_report_bundle(run_id, root=runs_root)
    report_path = bundle.manifest_path.parent / "report.html"
    render_report(bundle, report_path)

    warnings = list(bundle.warnings)
    opened = False
    if open_report:
        try:
            opened = bool(webbrowser.open_new_tab(report_path.as_uri()))
            if not opened:
                warnings.append("浏览器未确认打开 report.html。")
        except Exception as exc:  # pragma: no cover - defensive
            warnings.append(f"--open 失败: {exc}")

    payload = {
        "ok": True,
        "run_id": run_id,
        "report": str(report_path),
        "opened": opened,
        "warnings": warnings,
    }
    return 0, payload


@click.command(name="render")
@click.option("--run-id", required=True, help="要渲染报告的 run id.")
@click.option("--open", "open_report", is_flag=True, help="渲染后在本地浏览器打开 HTML。")
def render(run_id: str, open_report: bool) -> None:
    """基于本地 manifest/log/wandb/prom 生成单页 HTML 报告."""
    try:
        exit_code, payload = run_render(run_id=run_id, open_report=open_report)
    except Exception as exc:
        payload = {"ok": False, "run_id": run_id, "error": str(exc)}
        exit_code = 1
    click.echo(json.dumps(payload, ensure_ascii=False, indent=2))
    raise click.exceptions.Exit(exit_code)
