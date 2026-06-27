# actor_rollout_ref.rollout.max_num_seqs

- **参数名**：`actor_rollout_ref.rollout.max_num_seqs`
- **分类**：效率
- **中文解释**：控制 rollout 推理后端同时运行的最大序列/请求数；在 vLLM 中对应 `max_num_seqs`，在 SGLang/Ascend 映射中接近 `max_running_requests`。
- **常见值**：$((128))、16、384
- **来源环境变量**：ROLLOUT_MAX_NUM_SEQS
- **性能影响**：文档说明：Verl 性能调优文档建议在 GPU cache 利用率低时提高 `max_num_seqs` 或 `max_num_batched_tokens`，以增大解码阶段有效 batch 和并发；过高会增加 KV cache/OOM 风险。
- **精度影响**：机制推断：并发上限不改变采样参数；除非引起 OOM、请求截断或后端调度异常，通常不直接影响精度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:86` actor_rollout_ref.rollout.max_num_seqs=${rollout_max_num_seqs}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:181` actor_rollout_ref.rollout.max_num_seqs=${rollout_max_num_seqs}
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:163` actor_rollout_ref.rollout.max_num_seqs=16

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
