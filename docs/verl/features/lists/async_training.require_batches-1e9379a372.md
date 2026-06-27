# async_training.require_batches

- **参数名**：`async_training.require_batches`
- **分类**：效率
- **中文解释**：文档说明：fully_async_policy 中每次训练至少需要的 mini-batch 数，源码用 `actor.ppo_mini_batch_size * require_batches` 计算 required samples。
- **常见值**：1
- **来源环境变量**：REQUIRE_BATCHES
- **性能影响**：文档说明：官方 require_batches 消融显示该值会影响 streaming 每次发样数量、响应长度和训练时间；增大通常提升批量效率，但也会改变队列压力和等待节奏。
- **精度影响**：文档说明：官方消融提示发样数量会影响训练中的 response length，进而影响训练时间和结果；它不直接改奖励函数，但会改变异步样本组成与训练节奏。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:137` async_training.require_batches=${require_batches} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
