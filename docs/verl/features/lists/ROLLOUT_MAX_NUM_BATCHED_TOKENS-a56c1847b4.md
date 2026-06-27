# ROLLOUT_MAX_NUM_BATCHED_TOKENS

- **参数名**：`ROLLOUT_MAX_NUM_BATCHED_TOKENS`
- **分类**：效率
- **中文解释**：文档说明：示例环境变量，最终映射到 `actor_rollout_ref.rollout.max_num_batched_tokens`，限制 rollout 推理引擎一次 batch 可处理的最大 token 数。
- **常见值**：1024、10240、20000
- **来源环境变量**：ROLLOUT_MAX_NUM_BATCHED_TOKENS
- **性能影响**：文档说明：Verl 性能文档建议在 GPU cache 利用率低时增大 `max_num_batched_tokens` 以扩大解码阶段有效 batch，并建议高吞吐场景设置大于 2048；过大也会增加 KV cache/显存压力和 OOM 风险。
- **精度影响**：机制推断：通常不直接改变采样分布；若设置过小导致请求切分、吞吐瓶颈、OOM 或被迫缩短上下文，可能间接影响训练进度和结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:37` ROLLOUT_MAX_NUM_BATCHED_TOKENS=${ROLLOUT_MAX_NUM_BATCHED_TOKENS:-20000}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:58` rollout_max_num_batched_tokens=${ROLLOUT_MAX_NUM_BATCHED_TOKENS:-10240}
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:38` ROLLOUT_MAX_NUM_BATCHED_TOKENS=${ROLLOUT_MAX_NUM_BATCHED_TOKENS:-1024}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
