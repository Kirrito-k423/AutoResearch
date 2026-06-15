---
phase: 09-skill-08-experiment-report
plan: 01
status: completed
subsystem: experiment-report
tags: [report, manifest, loader, wandb, prometheus, logs]

requires:
  - phase: 08
    provides: [manifest, log, wandb_path, prom_pushed]
provides:
  - "autoresearch/report/models.py: ReportBundle + Log/Wandb/Prometheus 视图模型"
  - "autoresearch/report/loader.py: run_id -> ReportBundle"
  - "autoresearch/report/logs.py: 本地 log 摘要与 tail 提取"
  - "autoresearch/report/wandb.py: wandb-summary.json 读取 + 本地入口链接"
  - "autoresearch/report/prometheus.py: run_id 查询 + Prom graph 链接"
  - "5 个 Phase 9 loader 相关测试"
affects: [phase-09-experiment-report]

key-files:
  created:
    - autoresearch/report/__init__.py
    - autoresearch/report/models.py
    - autoresearch/report/loader.py
    - autoresearch/report/logs.py
    - autoresearch/report/wandb.py
    - autoresearch/report/prometheus.py
    - tests/test_report_loader.py
    - tests/test_report_wandb.py
    - tests/test_report_prometheus.py

requirements-completed:
  - RPT-MANIFEST-01
  - RPT-PAGE-02
  - RPT-LINK-01

duration: 40min
completed: 2026-06-15
---

# Phase 09 Plan 01: 读 manifest + 收集三路数据 Summary

Phase 9 的数据加载层已落地。现在可以从 `run_id` 直接读本地 `manifest/log/wandb/prom`，组合成 `ReportBundle`，并在某一路数据缺失时保持 partial-friendly，不会因为单路缺口而让报告生成整体失败。

## Accomplishments

### 1. `ReportBundle` 统一模型

新增 `autoresearch/report/models.py`，把报告渲染需要的输入统一成：

- `ReportBundle`
- `LogView`
- `WandbView`
- `PrometheusView`
- `ArtifactLink`
- `MetricPoint`

后续 HTML 渲染只消费这些模型，不再到处散读文件和 HTTP。

### 2. 本地 log / wandb / Prometheus 三路读取

- `autoresearch/report/logs.py`：提取 `SUM=` / `NPU_COUNT=` / `WANDB_RUN_ID=` 等关键行和 log tail
- `autoresearch/report/wandb.py`：读取 `wandb-summary.json`，生成 snapshot 指标和本地 W&B 入口链接
- `autoresearch/report/prometheus.py`：按 `run_id` 查询 `autoresearch_npu_count`，并构造固定 Prometheus graph URL

### 3. `load_report_bundle(run_id)`

`autoresearch/report/loader.py` 已实现：

```python
load_report_bundle(run_id, root=None) -> ReportBundle
```

流程：

1. 找 `manifest.json`
2. 读 log 摘要
3. 读 wandb summary
4. 读本地 Prometheus
5. 聚合 warnings / raw artifact links

## Verification

```bash
uv run pytest tests/test_report_loader.py tests/test_report_wandb.py tests/test_report_prometheus.py -q
```

结果：相关测试全部通过。

## Notes

- M1 的 wandb / prom 数据按 D-53 语义是 snapshot-style，不假装存在长时训练曲线。
- W&B deep-link 仍保持 best-effort；root URL + `wandb_run_id` 已稳定落盘。
