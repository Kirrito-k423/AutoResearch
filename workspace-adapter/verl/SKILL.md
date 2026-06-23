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
4. 生成不可变 `config.lock.json` 和 `provenance.lock.json`，记录所有参与仓的 commit / branch / GitHub 链接；默认使用当前分支，不按 run 自动创建新分支。
5. 真实 GRPO 训练从单卡 BS=1 开始调参，逐步增大 batch/micro-batch 等旋钮；每个 case 必须完成 3 个 training step，少于 3 步的结果只能记为失败数据点。
6. 稳定单卡候选再晋升到单机 8 卡吞吐 case；仍需保留每个 case 的 `completed_training_steps`、`target_training_steps`、失败类别、吞吐和资源曲线。
7. 交付件使用编号目录：`0-report/`、`1-wandb/`、`2-prometheus/`、`3-raw-logs/`、`4-config/`、`5-provenance/`、`6-rows/`、`restore/`；manifest 的 `artifact_layout` 是路径事实来源。
8. 报告必须说明 `trainer_val_only`：`true` 是验证矩阵，`false` 才进入真实 GRPO 训练。

## Git 管理约定

- 默认直接使用调用者当前分支，例如 `master`；不要为每次实验自动生成 `codex/verl-case-*` 分支。
- `--allow-git-push` 只负责把当前分支的 dirty state commit/push 并记录 commit SHA。
- 只有需要长期并行开发或 PR 隔离时，才由人显式创建新分支。
- 历史 `codex/verl-case-*` 分支不要自动删除，因为旧 `provenance.lock.json` 和报告中的 GitHub 链接可能还指向它们。

## TOP3 排错经验

1. **W&B 页面看起来没数据**：先确认 project 是否是 `verl`，run display name 是否按语义命名；再检查 `1-wandb/source-runs.json`、`1-wandb/rebuild-wandb.sh` 和全局 `rebuild-all.sh` 是否能重建历史 Web 视图。
2. **Prometheus 没有显存/Core 曲线或只是一条直线**：确认运行期是否持续采集 `npu-smi info`/watch 原始日志，并写入 `6-rows/cases/*/npu-smi-watch.raw.log`；同时确认训练进程运行时是否持续 push `autoresearch_npu_*` 与 `autoresearch_machine_npu_*` 到 Pushgateway。Pushgateway 只保存 latest gauge，run 后一次性 push 会让 Grafana 显示平线；报告应能从 `2-prometheus/telemetry-openmetrics.prom` 回放 0.5s 原始曲线。
3. **geo3k acc 为 0**：检查 `rows/*/validation/0.jsonl` 的 `output/gts/acc`。模型即使算出正确数值，若未按 reward 要求输出 `\\boxed{}`，严格 acc 仍可能为 0；val-only 不会更新模型参数。
