"""Render a single-file local HTML report."""
from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from .models import MetricPoint, ReportBundle


def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return "无"
    return value.isoformat().replace("+00:00", "Z")


def _format_elapsed_ms(bundle: ReportBundle) -> str:
    if bundle.one_step and isinstance(bundle.one_step.get("elapsed_ms"), (int, float)):
        return f"{int(bundle.one_step['elapsed_ms'])} ms"
    if bundle.finished_at is None:
        return "无"
    delta = bundle.finished_at - bundle.started_at
    return f"{int(delta.total_seconds() * 1000)} ms"


def _metric_svg(points: list[MetricPoint], *, width: int = 220, height: int = 72) -> str:
    if not points:
        return '<div class="empty">暂无指标数据</div>'
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
        return "无"
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
    ) or "<tr><td colspan='10'>暂无矩阵行</td></tr>"
    length_rows = "".join(
        "<tr>"
        f"<td>{item['output_tokens']}</td>"
        f"<td>{escape(_fmt_metric(item.get('success_rate'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('tokens_per_second')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('latency_ms')))}</td>"
        "</tr>"
        for item in view.length_summary
    ) or "<tr><td colspan='4'>暂无长度数据</td></tr>"
    async_rows = "".join(
        "<tr>"
        f"<td>{item['output_tokens']}</td>"
        f"<td>{escape(_fmt_metric(item.get('tokens_per_second_delta')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('latency_ms_delta')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('accuracy_delta'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('consistency_delta'), percent=True))}</td>"
        "</tr>"
        for item in view.async_comparison
    ) or "<tr><td colspan='5'>暂无 sync/async 配对数据</td></tr>"
    mode_rows = "".join(
        "<tr>"
        f"<td>{escape(str(item['mode']))}</td>"
        f"<td>{escape(_fmt_metric(item.get('success_rate'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('accuracy'), percent=True))}</td>"
        f"<td>{escape(_fmt_metric(item.get('tokens_per_second')))}</td>"
        f"<td>{escape(_fmt_metric(item.get('latency_ms')))}</td>"
        "</tr>"
        for item in view.mode_summary
    ) or "<tr><td colspan='5'>暂无模式数据</td></tr>"
    artifact_rows = "".join(
        "<tr>"
        f"<td>{escape(item.name)}</td>"
        f"<td>{'已找到' if item.ok else '缺失'}</td>"
        f"<td>{escape(str(item.path) if item.path else '')}</td>"
        f"<td>{escape(item.warning or '')}</td>"
        "</tr>"
        for item in view.artifacts
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in view.warnings) or "<li>无</li>"
    score_notes = "".join(f"<li>{escape(item)}</li>" for item in view.score_diagnostics) or "<li>无</li>"
    status = "完整" if view.complete_matrix else "不完整"
    return f"""
    <section class="section">
      <h2>Verl 正式 Case 矩阵</h2>
      <div class="note {'ok' if view.complete_matrix else 'error'}">矩阵状态: {escape(status)}</div>
      <div class="note">{escape(view.training_mode)}</div>
      <table>
        <thead><tr><th>输入</th><th>输出</th><th>模式</th><th>状态</th><th>Tokens/s</th><th>延迟 ms</th><th>样本</th><th>准确率</th><th>一致性</th><th>错误</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>

    <div class="section-grid">
      <section class="section">
        <h2>序列长度影响</h2>
        <table>
          <thead><tr><th>输出 Tokens</th><th>成功率</th><th>Tokens/s</th><th>延迟 ms</th></tr></thead>
          <tbody>{length_rows}</tbody>
        </table>
      </section>
      <section class="section">
        <h2>同步/异步影响</h2>
        <table>
          <thead><tr><th>输出 Tokens</th><th>Tokens/s 差值</th><th>延迟差值</th><th>准确率差值</th><th>一致性差值</th></tr></thead>
          <tbody>{async_rows}</tbody>
        </table>
      </section>
    </div>

    <div class="section-grid">
      <section class="section">
        <h2>准确率</h2>
        <p>整体: <strong>{escape(_fmt_metric(view.accuracy_overall, percent=True))}</strong></p>
        <table>
          <thead><tr><th>模式</th><th>成功率</th><th>准确率</th><th>Tokens/s</th><th>延迟 ms</th></tr></thead>
          <tbody>{mode_rows}</tbody>
        </table>
      </section>
      <section class="section">
        <h2>一致性与诊断</h2>
        <p>整体: <strong>{escape(_fmt_metric(view.consistency_overall, percent=True))}</strong></p>
        <h3>0 分诊断</h3>
        <ul>{score_notes}</ul>
        <h3>告警</h3>
        <ul>{warnings}</ul>
      </section>
    </div>

    <section class="section">
      <h2>交付件完整性</h2>
      <table>
        <thead><tr><th>交付件</th><th>状态</th><th>路径</th><th>说明</th></tr></thead>
        <tbody>{artifact_rows}</tbody>
      </table>
    </section>
    """


def _skills_section(bundle: ReportBundle) -> str:
    if not bundle.skills_used:
        return ""
    rows = "".join(
        "<tr>"
        f"<td>{escape(skill.name)}</td>"
        f"<td><code>{escape(skill.path)}</code></td>"
        f"<td>{escape(skill.purpose)}</td>"
        "</tr>"
        for skill in bundle.skills_used
    )
    return f"""
    <section class="section">
      <h2>本次使用的仓库 Skill</h2>
      <table>
        <thead><tr><th>Skill</th><th>位置</th><th>用途</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>
    """


def render_report(bundle: ReportBundle, output_path: Path) -> Path:
    """Write a single-file static HTML report and return its path."""
    if bundle.exit_code == 0 and not bundle.error and not bundle.warnings:
        status = "通过"
    elif bundle.exit_code == 0 and not bundle.error:
        status = "部分通过"
    else:
        status = "失败"
    summary_cards = [
        ("运行 ID", bundle.run_id),
        ("服务器", bundle.server),
        ("代码栈", bundle.lib),
        ("Conda 环境", bundle.conda_env or "无"),
        ("耗时", _format_elapsed_ms(bundle)),
        ("退出码", str(bundle.exit_code) if bundle.exit_code is not None else "无"),
        ("状态", status),
    ]
    if bundle.one_step:
        if bundle.one_step.get("sum") is not None:
            summary_cards.append(("SUM", f"{float(bundle.one_step['sum']):g}"))
        if bundle.one_step.get("npu_count") is not None:
            summary_cards.append(("NPU 数量", str(bundle.one_step["npu_count"])))

    artifact_links = "".join(
        f'<li><a href="{escape(link.href)}">{escape(link.label)}</a>'
        + (f' <span class="note">{escape(link.note)}</span>' if link.note else "")
        + "</li>"
        for link in bundle.artifact_links
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in bundle.warnings) or "<li>无</li>"
    key_lines = "".join(f"<li><code>{escape(line)}</code></li>" for line in bundle.log.key_lines) or "<li>无</li>"
    tail = "\n".join(bundle.log.tail_lines) if bundle.log.tail_lines else ""
    wandb_summary = "".join(
        f"<li><strong>{escape(str(key))}</strong>: {escape(str(value))}</li>"
        for key, value in bundle.wandb.summary.items()
        if not str(key).startswith("_")
    ) or "<li>暂无 summary 值</li>"
    prom_value = (
        f"{bundle.prometheus.current_value:g}"
        if bundle.prometheus.current_value is not None
        else "无"
    )
    wandb_links = "".join(
        f'<li><a href="{escape(link.href)}">{escape(link.label)}</a>'
        + (f' <span class="note">{escape(link.note)}</span>' if link.note else "")
        + "</li>"
        for link in bundle.wandb.links
    )
    wandb_run_links = "".join(
        f'<li><a href="{escape(link.href)}">{escape(link.label)}</a>'
        + (f' <span class="note">{escape(link.note)}</span>' if link.note else "")
        + "</li>"
        for link in bundle.wandb.run_links
    ) or "<li>暂无可链接的 W&B run</li>"
    prom_notes = "".join(f"<li>{escape(item)}</li>" for item in bundle.prometheus.notes) or "<li>无</li>"
    prom_evidence = (
        f'<li><strong>Evidence 文件</strong>: <code>{escape(str(bundle.prometheus.evidence_path))}</code></li>'
        if bundle.prometheus.evidence_path
        else ""
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AutoResearch 实验报告 {escape(bundle.run_id)}</title>
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
      <h1>AutoResearch 实验报告</h1>
      <div class="meta">
        <span>运行: <code>{escape(bundle.run_id)}</code></span>
        <span>开始: {escape(_format_datetime(bundle.started_at))}</span>
        <span>结束: {escape(_format_datetime(bundle.finished_at))}</span>
        <span>远程目录: <code>{escape(bundle.workdir_remote)}</code></span>
      </div>
      <div class="note">本报告从本地数据仓交付件渲染；实时服务不可用时，以 manifest、matrix、logs、wandb、prom evidence 为准。</div>
    </section>

    <section class="grid">
      {''.join(
          f'<div class="card"><div class="label">{escape(label)}</div><div class="value">{escape(value)}</div></div>'
          for label, value in summary_cards
      )}
    </section>

    <section class="section">
      <h2>告警</h2>
      <ul>{warnings}</ul>
      {"<p class='error'><strong>错误:</strong> " + escape(bundle.error) + "</p>" if bundle.error else ""}
    </section>

	    <section class="section">
	      <h2>原始交付件</h2>
	      <ul>{artifact_links}</ul>
	    </section>

	    {_formal_case_sections(bundle)}
	    {_skills_section(bundle)}

	    <div class="section-grid">
      <section class="section">
        <h2>日志视图</h2>
        <div class="note {'warning' if bundle.log.warning else 'ok'}">{escape(bundle.log.warning or '本地日志已加载。')}</div>
        <h3>关键行</h3>
        <ul>{key_lines}</ul>
        <h3>尾部片段</h3>
        <pre>{escape(tail or '暂无日志片段')}</pre>
      </section>

      <section class="section">
        <h2>W&B 视图</h2>
        <div class="note {'warning' if bundle.wandb.warning else 'ok'}">{escape(bundle.wandb.warning or '本地 W&B summary 已加载。')}</div>
        <ul>{wandb_summary}</ul>
        {_metric_svg(next(iter(bundle.wandb.charts.values()), []))}
        <h3>入口</h3>
        <ul>{wandb_links}</ul>
        <h3>历史 run</h3>
        <ul>{wandb_run_links}</ul>
      </section>
    </div>

    <section class="section">
      <h2>Prometheus 视图</h2>
      <div class="note {'warning' if bundle.prometheus.warning else 'ok'}">{escape(bundle.prometheus.warning or '本地 Prometheus 查询成功。')}</div>
      <ul>
        <li><strong>指标</strong>: <code>{escape(bundle.prometheus.metric_name)}</code></li>
        <li><strong>查询</strong>: <code>{escape(bundle.prometheus.query)}</code></li>
        <li><strong>当前值</strong>: {escape(prom_value)}</li>
        {prom_evidence}
        <li><a href="{escape(bundle.prometheus.query_url)}">打开 Prometheus 查询</a></li>
      </ul>
      <h3>采集说明</h3>
      <ul>{prom_notes}</ul>
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
