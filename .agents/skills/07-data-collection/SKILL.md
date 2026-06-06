# Skill 07: data-collection

> 跑最小实验 + wandb sync + log 采集 + prom push。

## Boundary

| Use | Don't Use |
|---|---|
| 跑 `trainer.train()` 1-2 步 (调 06 的 minimal_runner) | 报告渲染 (这是 08) |
| wandb offline → 本地 wandb sync | 跑用例前 stack 健康 (这是 06) |
| 远程 log 回传 (调 datalake/logs/collector) | 硬件 / 网络 / 远程服务 |
| prom push 远程 → 本地 pushgateway |  |

## 入口

```bash
python3 .agents/skills/07-data-collection/scripts/run_minimal.py \
  --config ./config/config.yaml --server nvidia-01 --run-id 2026-06-06-smoke-001
```

## 状态

⏳ **Phase 9 待开发**。
