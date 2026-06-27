# ROLLOUT_IS_BATCH_NORMALIZE

- **参数名**：`ROLLOUT_IS_BATCH_NORMALIZE`
- **分类**：效率
- **中文解释**：控制 `algorithm.rollout_correction.rollout_is_batch_normalize`，即是否在 batch 内把截断后的 IS 权重归一化到均值为 1；该归一化只作用于 IS 权重，不改变 rejection sampling 的 mask。
- **常见值**：true
- **来源环境变量**：ROLLOUT_IS_BATCH_NORMALIZE
- **性能影响**：机制推断：启用后多一次按 token 或 sequence 统计均值的 reduction，计算开销通常较小；分布式大 batch 下可能增加少量同步和张量操作成本。
- **精度影响**：文档说明：rollout correction 文档说明 batch normalize 会在截断后把平均 IS 权重调回 1，有助于降低梯度尺度方差；同时会改变权重整体尺度，属于稳定性与原始校正强度之间的取舍。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:41` ROLLOUT_IS_BATCH_NORMALIZE=${ROLLOUT_IS_BATCH_NORMALIZE:-true}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
