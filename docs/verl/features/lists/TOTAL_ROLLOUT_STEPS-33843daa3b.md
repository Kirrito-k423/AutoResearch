# TOTAL_ROLLOUT_STEPS

- **参数名**：`TOTAL_ROLLOUT_STEPS`
- **分类**：效率
- **中文解释**：控制 fully async 训练的 rollout 样本总预算，映射到 `rollout.total_rollout_steps`，同时该示例也用它作为 actor 学习率衰减步数 `actor_rollout_ref.actor.optim.lr_decay_steps`。
- **常见值**：51200
- **来源环境变量**：TOTAL_ROLLOUT_STEPS
- **性能影响**：文档说明：fully async 文档将 `rollout.total_rollout_steps` 定义为 rollout 样本总数；数值越大，rollout、训练和验证总耗时近似增加，也会延长队列/日志/检查点周期。
- **精度影响**：机制推断：该值决定训练样本预算和学习率衰减 horizon；过小可能欠训练，过大增加过拟合或策略漂移风险，且会改变与同步/异步实验的可比性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:45` total_rollout_steps=${TOTAL_ROLLOUT_STEPS:-51200}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
