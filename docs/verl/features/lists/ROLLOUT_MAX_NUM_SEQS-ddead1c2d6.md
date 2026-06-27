# ROLLOUT_MAX_NUM_SEQS

- **参数名**：`ROLLOUT_MAX_NUM_SEQS`
- **分类**：效率
- **中文解释**：控制 `actor_rollout_ref.rollout.max_num_seqs`，限制 rollout 推理后端同时运行的最大序列/请求数；示例会按推理 TP 大小在 1024 与 384 之间给默认值。
- **常见值**：1024、384
- **来源环境变量**：ROLLOUT_MAX_NUM_SEQS
- **性能影响**：文档说明：Verl 性能调优文档建议在 GPU cache 利用率低时调大 `max_num_seqs` 或 `max_num_batched_tokens`，以提高解码阶段有效 batch 和并发；过高会增加 KV cache 与 OOM 风险。
- **精度影响**：机制推断：并发上限不改变采样分布；只有在引发 OOM、请求失败、超时或后端调度异常时，才会间接影响训练/验证结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:90` rollout_max_num_seqs=${ROLLOUT_MAX_NUM_SEQS:-1024}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:92` rollout_max_num_seqs=${ROLLOUT_MAX_NUM_SEQS:-384}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
