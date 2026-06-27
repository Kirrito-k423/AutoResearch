---
name: train-stack-health
description: Inspect remote training stack health for conda envs, verl or veomni versions, and minimal one-step training smoke tests. Use when validating training dependencies, stack probe outputs, minimal runner behavior, or train stack readiness before data collection.
---

# Skill 06: train-stack-health

> 探测 conda env + verl/veomni 版本 + 跑 1-step 最小用例。

## Boundary

| Use | Don't Use |
|---|---|
| `conda env list` + `pip list` 解析 | 远程硬件 (这是 03) |
| 跑 verl/veomni 1-step 烟雾用例 | 网络测速 (这是 04) |
| 验证 min 1 step 跑通 + loss 下降 | 远程服务可达 (这是 05) |
| 输出 train stack 健康表 | 报告渲染 |

## 入口

```bash
python3 .agents/skills/06-train-stack-health/scripts/stack_probe.py \
  --config ./config/config.yaml --server nvidia-01
```

## 状态

⏳ **Phase 8 待开发**。
