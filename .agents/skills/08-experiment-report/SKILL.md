# Skill 08: experiment-report

> 单页 HTML 报告 (log / wandb / prom 三视图)。

## Boundary

| Use | Don't Use |
|---|---|
| 读 manifest (调 datalake/manifest) | 任何采集 (这是 07) |
| 渲染 wandb 曲线截图 / 表格 | 跑用例 / 跑 stack |
| 渲染 prom 资源曲线 | 改配置 / 改密钥 |
| 渲染 log 关键事件 timeline |  |
| 展示本次使用的 repo skill 和交付件完整性 | 修改训练脚本行为 |
| 对 val-only / train 模式、0 分原因、Prometheus 缺指标给出诊断 | 把诊断当成新的实验结论 |

## 报告可读性规范

- 报告面向本地中文使用者，用户可见文案默认中文。
- 顶部必须说明数据来源：manifest、matrix、logs、wandb、prom evidence；实时服务不可用时，报告不能直接判定实验无数据。
- Formal Verl Case 必须显示：
  - 是否 `trainer_val_only=True`；
  - 矩阵完整性和每行状态；
  - 序列长度影响、sync/async 对比、准确率/一致性；
  - W&B Web run 链接和 raw offline run 恢复入口；
  - Prometheus evidence 中已推/缺失的指标；
  - 本次使用的 `.agents/skills/01..08` 和 `workspace-adapter/verl`。
- 交付件路径优先从数据包本地解析；旧 manifest 中的绝对路径只作为线索，不作为唯一真相。

## 本次 TOP3 问题沉淀

1. **英文报告影响交付阅读**：报告标题、表头、告警、诊断和交付件说明全部中文化；机器 key 保持英文稳定。
2. **验证矩阵被误读成 GRPO 训练**：只要 `trainer_val_only=True`，报告必须明确标为“验证矩阵”，并提示不会更新模型参数。
3. **0 分需要可解释**：报告要引导查看 `rows/*/validation/0.jsonl` 的 `output/gts/acc`；严格 reward 可能因未输出 `\\boxed{}` 或抽取失败记为 0。

## 入口

```bash
python3 .agents/skills/08-experiment-report/scripts/render_report.py \
  --run-id 2026-06-06-smoke-001 --open
```

## 状态

✅ **Phase 10 已具备 formal case 中文报告骨架；后续补资源曲线后继续扩展 Prometheus 图表。**
