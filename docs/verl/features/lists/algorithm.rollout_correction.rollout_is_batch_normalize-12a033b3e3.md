# algorithm.rollout_correction.rollout_is_batch_normalize

- **参数名**：`algorithm.rollout_correction.rollout_is_batch_normalize`
- **分类**：效率
- **中文解释**：控制是否在 batch 内把 IS 权重归一化到均值为 1；归一化发生在截断之后，只影响 IS 权重，不影响 rejection sampling。
- **常见值**："false"、"true"、true
- **来源环境变量**：ROLLOUT_IS_BATCH_NORMALIZE
- **性能影响**：机制推断：增加一次按 token 或按 sequence 的均值归一化/reduction，计算开销较小，但分布式场景可能多一次同步统计。
- **精度影响**：文档说明：rollout correction 文档说明该开关通过让 batch 平均权重为 1 来降低方差，同时会改变截断后权重的整体尺度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:74` algorithm.rollout_correction.rollout_is_batch_normalize=${rollout_is_batch_normalize}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:71` algorithm.rollout_correction.rollout_is_batch_normalize=${rollout_is_batch_normalize}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:86` algorithm.rollout_correction.rollout_is_batch_normalize=${ROLLOUT_IS_BATCH_NORMALIZE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
