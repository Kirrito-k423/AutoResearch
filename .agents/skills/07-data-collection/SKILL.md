# Skill 07: data-collection

> 跑最小实验 + wandb sync + log 采集 + prom push。

## Boundary

| Use | Don't Use |
|---|---|
| 跑 `trainer.train()` 1-2 步 (调 06 的 minimal_runner) | 报告渲染 (这是 08) |
| wandb offline → 本地 wandb sync | 跑用例前 stack 健康 (这是 06) |
| 远程 log 回传 (调 datalake/logs/collector) | 硬件 / 网络 / 远程服务 |
| prom push 远程 → 本地 pushgateway | 把实时 Prometheus 当成唯一证据源 |
| 写入不可变 evidence / manifest / config lock | 渲染最终报告 (这是 08) |

## Formal Verl Case 要求

- W&B 项目名使用代码栈名，例如 `verl`；run display name 使用 `模型-规模-算法-序列长度-时间-其余配置`，例如 `Qwen35-2B-GRPO-1Kto16K-260622d-145001s-valonly-sync-noignoreeos`。
- 数据仓必须保存 raw W&B offline runs、`runs.json`、`rebuild-wandb.sh`，保证复制数据仓后能重建同一个本地 W&B Web 视图。
- Prometheus 采集必须区分两类证据：实时 query 结果和本地 `prom/*.json` evidence。当前只推 `autoresearch_npu_count` 时，必须在 evidence 里显式记录缺少 HBM/Core 利用率。
- `manifest.json` 里的旧绝对路径不能作为唯一定位方式；报告和恢复脚本应能从数据包本地 `logs/`、`wandb/`、`prom/`、`rows/` 回退加载。

## 本次 TOP3 问题沉淀

1. **W&B 可读性不足**：project/run 命名要按实验语义组织，project 用 `verl`，run 名包含模型、规模、算法、序列长度、秒级时间和关键配置。
2. **Prometheus 空图误导**：没有采集 HBM/Core 时，不要在报告里假装资源曲线存在；必须写明已推指标和缺失指标。
3. **数据仓可复制性**：`autoresearch-log` 保存的是交付证据，不应依赖 `/Users/Zhuanz/.autoresearch` 的旧路径；加载器要支持 bundle-local fallback。

## 入口

```bash
python3 .agents/skills/07-data-collection/scripts/run_minimal.py \
  --config ./config/config.yaml --server nvidia-01 --run-id 2026-06-06-smoke-001
```

## 状态

✅ **Phase 9 已具备 formal case 数据采集骨架；资源利用率采集仍需接入 NPU exporter 或 npu-smi 采样。**
