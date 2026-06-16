"""Render a single-file local HTML report."""
from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from .models import MetricPoint, ReportBundle


def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return "N/A"
    return value.isoformat().replace("+00:00", "Z")


def _format_elapsed_ms(bundle: ReportBundle) -> str:
    if bundle.one_step and isinstance(bundle.one_step.get("elapsed_ms"), (int, float)):
        return f"{int(bundle.one_step['elapsed_ms'])} ms"
    if bundle.finished_at is None:
        return "N/A"
    delta = bundle.finished_at - bundle.started_at
    return f"{int(delta.total_seconds() * 1000)} ms"


def _metric_svg(points: list[MetricPoint], *, width: int = 220, height: int = 72) -> str:
    if not points:
        return '<div class="empty">No metric data</div>'
    if len(points) == 1:
        point = points[0]
        label = escape(f"{point.y:g}")
        return (
            f'<svg viewBox="0 0 {width} {height}" class="chart" role="img" '
            f'aria-label="{label}">'
            f'<line x1="24" y1="{height - 20}" x2="{width - 24}" y2="{height - 20}" '
            f'stroke="#cbd5e1" stroke-width="2"/>'
            f'<circle cx="{width / 2:.1f}" cy="{height / 2:.1f}" r="6" fill="#2563eb"/>'
            f'<text x="{width / 2:.1f}" y="{height / 2 - 14:.1f}" text-anchor="middle" '
            f'fill="#0f172a" font-size="12">{label}</text>'
            f"</svg>"
        )

    xs = [p.x for p in points]
    ys = [p.y for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    if max_x == min_x:
        max_x += 1
    if max_y == min_y:
        max_y += 1
    coords = []
    for point in points:
        x = 20 + ((point.x - min_x) / (max_x - min_x)) * (width - 40)
        y = height - 16 - ((point.y - min_y) / (max_y - min_y)) * (height - 32)
        coords.append((x, y))
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    circles = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#2563eb"/>' for x, y in coords
    )
    return (
        f'<svg viewBox="0 0 {width} {height}" class="chart" role="img" aria-label="metric chart">'
        f'<polyline points="{polyline}" fill="none" stroke="#2563eb" stroke-width="2"/>'
        f"{circles}</svg>"
    )


def _fmt_metric(value: float | None, *, percent: bool = False) -> str:
    if value is None:
        return "N/A"
    if percent:
        return f"{value * 100:.1f}%"
    return f"{value:.2f}"


def _formal_case_sections(bundle: ReportBundle) -> str:
    view = bundle.formal_case
    if view is None:
        return ""
    rows = "".join(
        "<tr>"
        f"<td>{row.input_tokens}</td>"
        f"<td>{row.output_tokens}</td>"
        f"<td>{escape(row.mode)}</td>"
        f"<td>{escape(row.status)}</td>"
        f"<td>{escape(_fmt_metric(row.tokens_per_second))}</td>"
        f"<td>{escape(_fmt_metric(row.latency_ms))}</td>"
        f"<td>{row.sample_count}</td>"
        f"<td>{escape(_fmt_metric(row.accuracy, percent=True))}</td>"
        f"<td>{escape(_fmt_metric(row.consistency, percent=True))}</td>"
        f"<td>{escape(row.error or '')}</td>"
        "</tr>"
        for row in view.rows
    ) or "<tr><td colspan='10'>No matrix rows</td></tr>"
    length_rows = "".join(
        "<tr>"
        f"<td>{item['output_tokens']}</td>"
        f"<td>{escape(_fmt_metric(item.get('success_rate'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('tokens_per_second')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('latency_ms')))}</td>"
        "</tr>"
        for item in view.length_summary
    ) or "<tr><td colspan='4'>No length data</td></tr>"
    async_rows = "".join(
        "<tr>"
        f"<td>{item['output_tokens']}</td>"
        f"<td>{escape(_fmt_metric(item.get('tokens_per_second_delta')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('latency_ms_delta')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('accuracy_delta'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('consistency_delta'), percent=True))}</td>"
        "</tr>"
        for item in view.async_comparison
    ) or "<tr><td colspan='5'>No paired sync/async data</td></tr>"
    mode_rows = "".join(
        "<tr>"
        f"<td>{escape(str(item['mode']))}</td>"
        f"<td>{escape(_fmt_metric(item.get('success_rate'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('accuracy'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('tokens_per_second')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('latency_ms')))}</td>"
        "</tr>"
        for item in view.mode_summary
    ) or "<tr><td colspan='5'>No mode data</td></tr>"
    artifact_rows = "".join(
        "<tr>"
        f"<td>{escape(item.name)}</td>"
        f"<td>{'OK' if item.ok else 'Missing'}</td>"
        f"<td>{escape(str(item.path) if item.path else '')}</td>"
        f"<td>{escape(item.warning or '')}</td>"
        "</tr>"
        for item in view.artifacts
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in view.warnings) or "<li>None</li>"
    status = "complete" if view.complete_matrix else "incomplete"
    return f"""
    <section class="section">
      <h2>Verl Formal Case Matrix</h2>
      <div class="note {'ok' if view.complete_matrix else 'error'}">Matrix status: {escape(status)}</div>
      <table>
        <thead><tr><th>Input</th><th>Output</th><th>Mode</th><th>Status</th><th>Tokens/s</th><th>Latency ms</th><th>Samples</th><th>Accuracy</th><th>Consistency</th><th>Error</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>

    <div class="section-grid">
      <section class="section">
        <h2>Sequence Length Impact</h2>
        <table>
          <thead><tr><th>Output Tokens</th><th>Success</th><th>Tokens/s</th><th>Latency ms</th></tr></thead>
          <tbody>{length_rows}</tbody>
        </table>
      </section>
      <section class="section">
        <h2>Sync vs Async Impact</h2>
        <table>
          <thead><tr><th>Output Tokens</th><th>Tokens/s Delta</th><th>Latency Delta</th><th>Accuracy Delta</th><th>Consistency Delta</th></tr></thead>
          <tbody>{async_rows}</tbody>
        </table>
      </section>
    </div>

    <div class="section-grid">
      <section class="section">
        <h2>Accuracy</h2>
        <p>Overall: <strong>{escape(_fmt_metric(view.accuracy_overall, percent=True))}</strong></p>
        <table>
          <thead><tr><th>Mode</th><th>Success</th><th>Accuracy</th><th>Tokens/s</th><th>Latency ms</th></tr></thead>
          <tbody>{mode_rows}</tbody>
        </table>
      </section>
      <section class="section">
        <h2>Consistency</h2>
        <p>Overall: <strong>{escape(_fmt_metric(view.consistency_overall, percent=True))}</strong></p>
        <h3>Warnings</h3>
        <ul>{warnings}</ul>
      </section>
    </div>

    <section class="section">
      <h2>Provenance</h2>
      <table>
        <thead><tr><th>Artifact</th><th>Status</th><th>Path</th><th>Warning</th></tr></thead>
        <tbody>{artifact_rows}</tbody>
      </table>
    </section>
    """


def render_report(bundle: ReportBundle, output_path: Path) -> Path:
    """Write a single-file static HTML report and return its path."""
    if bundle.exit_code == 0 and not bundle.error and not bundle.warnings:
        status = "PASS"
    elif bundle.exit_code == 0 and not bundle.error:
        status = "PARTIAL"
    else:
        status = "FAIL"
    summary_cards = [
        ("Run ID", bundle.run_id),
        ("Server", bundle.server),
        ("Lib", bundle.lib),
        ("Conda Env", bundle.conda_env or "N/A"),
        ("Elapsed", _format_elapsed_ms(bundle)),
        ("Exit", str(bundle.exit_code) if bundle.exit_code is not None else "N/A"),
        ("Status", status),
    ]
    if bundle.one_step:
        if bundle.one_step.get("sum") is not None:
            summary_cards.append(("SUM", f"{float(bundle.one_step['sum']):g}"))
        if bundle.one_step.get("npu_count") is not None:
            summary_cards.append(("NPU Count", str(bundle.one_step["npu_count"])))

    artifact_links = "".join(
        f'<li><a href="{escape(link.href)}">{escape(link.label)}</a>'
        + (f' <span class="note">{escape(link.note)}</span>' if link.note else "")
        + "</li>"
        for link in bundle.artifact_links
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in bundle.warnings) or "<li>None</li>"
    key_lines = "".join(f"<li><code>{escape(line)}</code></li>" for line in bundle.log.key_lines) or "<li>None</li>"
    tail = "\n".join(bundle.log.tail_lines) if bundle.log.tail_lines else ""
    wandb_summary = "".join(
        f"<li><strong>{escape(str(key))}</strong>: {escape(str(value))}</li>"
        for key, value in bundle.wandb.summary.items()
        if not str(key).startswith("_")
    ) or "<li>No summary values</li>"
    prom_value = (
        f"{bundle.prometheus.current_value:g}"
        if bundle.prometheus.current_value is not None
        else "N/A"
    )
    wandb_links = "".join(
        f'<li><a href="{escape(link.href)}">{escape(link.label)}</a>'
        + (f' <span class="note">{escape(link.note)}</span>' if link.note else "")
        + "</li>"
        for link in bundle.wandb.links
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AutoResearch Report {escape(bundle.run_id)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f8fafc;
      --panel: #ffffff;
      --text: #0f172a;
      --muted: #475569;
      --line: #dbe4ee;
      --blue: #2563eb;
      --amber: #b45309;
      --red: #b91c1c;
      --green: #15803d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    h1, h2, h3 {{ margin: 0 0 12px; }}
    .header {{
      display: grid;
      gap: 12px;
      margin-bottom: 20px;
    }}
    .meta {{
      color: var(--muted);
      font-size: 14px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px 16px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin: 20px 0 28px;
    }}
    .card, .section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .card {{ padding: 14px; min-height: 92px; }}
    .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; }}
    .value {{ font-size: 20px; margin-top: 8px; font-weight: 600; word-break: break-word; }}
    .section {{ padding: 18px; margin-bottom: 16px; }}
    .section-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }}
    .note {{ color: var(--muted); font-size: 13px; }}
    .warning {{ color: var(--amber); }}
    .error {{ color: var(--red); }}
    .ok {{ color: var(--green); }}
    ul {{ margin: 8px 0 0; padding-left: 18px; }}
    code, pre {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      background: #eff6ff;
      border-radius: 4px;
    }}
    code {{ padding: 1px 4px; }}
    pre {{
      margin: 8px 0 0;
      padding: 12px;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }}
	    .chart {{
      width: 100%;
      max-width: 260px;
      height: auto;
      display: block;
      margin-top: 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #f8fafc;
    }}
	    .empty {{
      margin-top: 12px;
      padding: 14px;
      border: 1px dashed var(--line);
      border-radius: 6px;
      color: var(--muted);
      font-size: 14px;
    }}
	    a {{ color: var(--blue); text-decoration: none; }}
	    a:hover {{ text-decoration: underline; }}
	    table {{
	      width: 100%;
	      border-collapse: collapse;
	      margin-top: 10px;
	      font-size: 14px;
	    }}
	    th, td {{
	      border-bottom: 1px solid var(--line);
	      padding: 8px 6px;
	      text-align: left;
	      vertical-align: top;
	    }}
	    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; }}
	  </style>
</head>
<body>
  <main>
    <section class="header">
      <h1>AutoResearch Experiment Report</h1>
      <div class="meta">
        <span>Run: <code>{escape(bundle.run_id)}</code></span>
        <span>Started: {escape(_format_datetime(bundle.started_at))}</span>
        <span>Finished: {escape(_format_datetime(bundle.finished_at))}</span>
        <span>Remote workdir: <code>{escape(bundle.workdir_remote)}</code></span>
      </div>
      <div class="note">Phase 8 minimal-run snapshot. Metrics may be single-point by design.</div>
    </section>

    <section class="grid">
      {''.join(
          f'<div class="card"><div class="label">{escape(label)}</div><div class="value">{escape(value)}</div></div>'
          for label, value in summary_cards
      )}
    </section>

    <section class="section">
      <h2>Warnings</h2>
      <ul>{warnings}</ul>
      {"<p class='error'><strong>Error:</strong> " + escape(bundle.error) + "</p>" if bundle.error else ""}
    </section>

	    <section class="section">
	      <h2>Raw Artifacts</h2>
	      <ul>{artifact_links}</ul>
	    </section>

	    {_formal_case_sections(bundle)}

	    <div class="section-grid">
      <section class="section">
        <h2>Log View</h2>
        <div class="note {'warning' if bundle.log.warning else 'ok'}">{escape(bundle.log.warning or 'Local log loaded.')}</div>
        <h3>Key Lines</h3>
        <ul>{key_lines}</ul>
        <h3>Tail Excerpt</h3>
        <pre>{escape(tail or 'No log excerpt')}</pre>
      </section>

      <section class="section">
        <h2>W&B View</h2>
        <div class="note {'warning' if bundle.wandb.warning else 'ok'}">{escape(bundle.wandb.warning or 'Local wandb summary loaded.')}</div>
        <ul>{wandb_summary}</ul>
        {_metric_svg(bundle.wandb.charts.get('sum', []))}
        <h3>Links</h3>
        <ul>{wandb_links}</ul>
      </section>
    </div>

    <section class="section">
      <h2>Prometheus View</h2>
      <div class="note {'warning' if bundle.prometheus.warning else 'ok'}">{escape(bundle.prometheus.warning or 'Local Prometheus query succeeded.')}</div>
      <ul>
        <li><strong>Metric</strong>: <code>{escape(bundle.prometheus.metric_name)}</code></li>
        <li><strong>Query</strong>: <code>{escape(bundle.prometheus.query)}</code></li>
        <li><strong>Current value</strong>: {escape(prom_value)}</li>
        <li><a href="{escape(bundle.prometheus.query_url)}">Open Prometheus query</a></li>
      </ul>
      {_metric_svg(bundle.prometheus.series)}
    </section>
  </main>
</body>
</html>
"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
