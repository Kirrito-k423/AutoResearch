# algorithm.rollout_correction.rollout_is

- **参数名**：`algorithm.rollout_correction.rollout_is`
- **分类**：效率
- **中文解释**：Rollout Correction 中的 importance sampling（IS）权重聚合级别；`token` 表示逐 token 权重，`sequence` 表示整段回复共享序列级权重，`null` 则关闭 IS。
- **常见值**："sequence"、"token"、sequence
- **来源环境变量**：ROLLOUT_IS
- **性能影响**：机制推断：需要根据 rollout policy 与训练 policy 的 logprob 计算权重并记录指标，带来少量张量计算和内存开销；相对 rollout 生成成本通常较小。
- **精度影响**：文档说明：源码注释说明 IS 用于修正 off-policy 分布偏移；`token` 偏低方差但有偏，`sequence` 更接近无偏但方差更高，直接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:72` algorithm.rollout_correction.rollout_is=${rollout_is}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:69` algorithm.rollout_correction.rollout_is=${rollout_is}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:84` algorithm.rollout_correction.rollout_is=${ROLLOUT_IS}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
