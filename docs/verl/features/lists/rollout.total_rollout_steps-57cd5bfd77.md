# rollout.total_rollout_steps

- **参数名**：`rollout.total_rollout_steps`
- **分类**：效率
- **中文解释**：文档说明：fully async policy 中 Rollouter 需要生成的 rollout 样本总数；官方说明可用 `data.train_batch_size * step` 与 colocate 训练的样本规模对齐。
- **常见值**：51200
- **来源环境变量**：TOTAL_ROLLOUT_STEPS
- **性能影响**：文档说明：该值直接决定异步 rollout 总生产量和运行时长；更大值会增加 rollout 计算、队列占用和参数同步周期数，过小则可能不足以跑满计划训练步数。
- **精度影响**：机制推断：不改变单样本目标函数，但决定 RL 训练可用样本/更新规模；样本总数过少会影响收敛与评估可信度，过多则增加 stale sample 管理压力。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:132` rollout.total_rollout_steps=${total_rollout_steps} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
