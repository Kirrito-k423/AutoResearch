---
phase: 09-skill-08-experiment-report
plan: 02
status: completed
subsystem: experiment-report
tags: [report, html, cli, open]

requires:
  - phase: 09-01
    provides: [ReportBundle]
provides:
  - "autoresearch/report/render.py: 单文件静态 HTML 渲染"
  - "autoresearch/report/cli.py: `autoresearch report render --run-id X [--open]`"
  - "autoresearch/cli.py: 新增 report group"
  - "tests/test_report_render.py + tests/test_report_cli.py"
  - "真实 run 的 report.html 产物与 `--open` 验证"
affects: [phase-09-experiment-report]

key-files:
  created:
    - autoresearch/report/render.py
    - autoresearch/report/cli.py
    - tests/test_report_render.py
    - tests/test_report_cli.py
  modified:
    - autoresearch/cli.py

requirements-completed:
  - RPT-PAGE-01
  - RPT-PAGE-02
  - RPT-PAGE-03
  - RPT-LINK-01

duration: 35min
completed: 2026-06-15
---

# Phase 09 Plan 02: HTML 模板 + 嵌入图表 + 浏览器打开 Summary

`autoresearch report render` 已可基于本地 `ReportBundle` 生成单页 HTML，并支持 `--open` 在浏览器打开。报告首屏展示 run 摘要，下方分区展示 log、W&B、Prometheus 和 raw artifact links。

## Accomplishments

### 1. 单文件静态 HTML

`autoresearch/report/render.py` 会把 `ReportBundle` 落到：

```text
~/.autoresearch/runs/<run_id>/report.html
```

页面包含：

- summary cards
- warnings / error
- raw artifact links
- `Log View`
- `W&B View`
- `Prometheus View`

图表采用轻量 snapshot 风格 SVG，满足 M1 最小实验的数据粒度。

### 2. report CLI

新增：

```bash
autoresearch report render --run-id X
autoresearch report render --run-id X --open
```

最终 stdout 仍保持唯一 JSON，包含：

- `ok`
- `run_id`
- `report`
- `opened`
- `warnings`

### 3. 顶层 CLI 接线

`autoresearch/cli.py` 已新增 `report` group，和 `collect/services/...` 保持同级入口。

## Verification

```bash
uv run pytest tests/test_report_render.py tests/test_report_cli.py -q
```

结果：相关测试全部通过。

## Real UAT

真实 run：

```bash
uv run autoresearch report render --run-id 01KV5MV7N5A3RBZ6388E5HCYAP
uv run autoresearch report render --run-id 01KV5MV7N5A3RBZ6388E5HCYAP --open
```

结果：

- `report.html` 生成成功
- `opened=true`
- 报告文件中包含 `AutoResearch Experiment Report` / `Log View` / `W&B View` / `Prometheus View`

报告路径：

```text
/Users/Zhuanz/.autoresearch/runs/01KV5MV7N5A3RBZ6388E5HCYAP/report.html
```
