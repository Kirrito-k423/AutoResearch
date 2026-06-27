# actor_rollout_ref.actor.optim.lr_decay_steps

- **参数名**：`actor_rollout_ref.actor.optim.lr_decay_steps`
- **分类**：算法
- **中文解释**：文档说明：Actor optimizer 的学习率衰减步数；Verl 配置文档说明 Megatron optimizer 在 warmup 之后按 `lr_decay_style` 在 `lr_decay_steps` 范围内把学习率衰减到 `min_lr`。
- **常见值**：51200
- **来源环境变量**：TOTAL_ROLLOUT_STEPS
- **性能影响**：机制推断：不直接改变单步计算量；但会影响达到目标指标所需训练步数、稳定窗口和端到端训练成本。
- **精度影响**：机制推断：衰减步数过短会让学习率过早变小，可能欠拟合或探索不足；过长则后期学习率偏高，可能带来震荡。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:87` actor_rollout_ref.actor.optim.lr_decay_steps=${total_rollout_steps} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
