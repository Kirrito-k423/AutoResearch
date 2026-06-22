# Skill: workspace-adapter/verl

> Verl GRPO 正式 case 的训练栈适配层，负责把 AutoResearch 的 1-8 skill 串到 Verl 容器、数据、模型、W&B、Prometheus 和报告交付件上。

## Boundary

| Use | Don't Use |
|---|---|
| 构造 `autoresearch run verl-case` 的正式矩阵 | 管理通用 SSH / secret / layout |
| 同步 verl/vllm/transformers/mindspeed 等依赖仓并记录 commit | 维护本地服务 compose |
| 生成 Qwen/geo3k/GRPO 的不可变 config lock | 修改数据仓总目录结构 |
| 解释 val-only、真实 GRPO 训练、严格 reward/acc 的边界 | 把验证矩阵结果包装成训练收益 |

## 命名规范

- W&B project 使用代码仓或训练栈名，例如 `verl`。
- W&B run display name 使用：`模型-规模-算法-序列长度-时间-其余配置`。
- 示例：`Qwen35-2B-GRPO-1Kto16K-260622d-145001s-valonly-sync-noignoreeos`。
- 数据包目录使用同一语义，但可以把多模式合并成 `modes-sync-async`。

## Formal Case 流程

1. 读取客户配置和数据仓根目录，确认 `cache_root`、`artifact_root`、`wandb_project` 可配置。
2. 跑 1-6 readiness，选择满足 Docker/NPU/网络/训练栈要求的远程机器。
3. 准备 Qwen3.5-2B 和 `hiyouga/geometry3k`，5GB 内允许本地缓存。
4. 生成不可变 `config.lock.json` 和 `provenance.lock.json`，记录所有参与仓的 commit / branch / GitHub 链接。
5. 运行 1K prompt 到 2K/4K/8K/16K response，sync/async 成对矩阵，`ignore_eos=false`。
6. 采集 `matrix-results.jsonl`、`rows/`、`logs/`、`wandb/`、`prom/`、`reports/`、`restore/`。
7. 报告必须说明 `trainer_val_only`：`true` 是验证矩阵，`false` 才进入真实 GRPO 训练。

## TOP3 排错经验

1. **W&B 页面看起来没数据**：先确认 project 是否是 `verl`，run display name 是否按语义命名；再检查 `wandb/runs.json` 和全局 `wandb/rebuild-all.sh` 是否能重建历史 Web 视图。
2. **Prometheus 没有显存/Core 曲线**：当前只推 `autoresearch_npu_count` 就只能证明 NPU 数量；HBM/Core 必须新增采样指标，例如 `autoresearch_npu_hbm_used_mib`、`autoresearch_npu_hbm_total_mib`、`autoresearch_npu_aicore_utilization_percent`。
3. **geo3k acc 为 0**：检查 `rows/*/validation/0.jsonl` 的 `output/gts/acc`。模型即使算出正确数值，若未按 reward 要求输出 `\\boxed{}`，严格 acc 仍可能为 0；val-only 不会更新模型参数。
