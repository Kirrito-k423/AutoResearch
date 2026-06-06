# Skill 08: experiment-report

> 单页 HTML 报告 (log / wandb / prom 三视图)。

## Boundary

| Use | Don't Use |
|---|---|
| 读 manifest (调 datalake/manifest) | 任何采集 (这是 07) |
| 渲染 wandb 曲线截图 / 表格 | 跑用例 / 跑 stack |
| 渲染 prom 资源曲线 | 改配置 / 改密钥 |
| 渲染 log 关键事件 timeline |  |

## 入口

```bash
python3 .agents/skills/08-experiment-report/scripts/render_report.py \
  --run-id 2026-06-06-smoke-001 --open
```

## 状态

⏳ **Phase 10 待开发**。
