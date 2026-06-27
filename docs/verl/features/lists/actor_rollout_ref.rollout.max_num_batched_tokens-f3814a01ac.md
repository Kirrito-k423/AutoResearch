# actor_rollout_ref.rollout.max_num_batched_tokens

- **参数名**：`actor_rollout_ref.rollout.max_num_batched_tokens`
- **分类**：效率
- **中文解释**：文档说明：vLLM rollout 每批可调度的最大 token 数，用于控制 decode/prefill 的有效 batch token 容量，常与 chunked prefill 一起调优。
- **常见值**：$((1024))、$((max_prompt_length + max_response_length))、$max_num_batched_tokens、1024、10240、20000、2048、32768、8192
- **来源环境变量**：ROLLOUT_MAX_NUM_BATCHED_TOKENS
- **性能影响**：文档说明：GPU cache 利用率低时增大该值可提高并发和吞吐；官方建议实际值至少大于 2048，Best Practices 给出 `max(8192, max_prompt_length + max_response_length, max_model_len)` 的经验规则。
- **精度影响**：机制推断：不改变采样分布；过低可能限制并发和长样本处理，过高则增加 KV cache/显存压力并引发 OOM。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：16
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tutorial/skypilot/verl-grpo.yaml`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:112` actor_rollout_ref.rollout.max_num_batched_tokens=$((max_prompt_length + max_response_length)) \
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:123` actor_rollout_ref.rollout.max_num_batched_tokens=$((max_prompt_length + max_response_length))
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:116` actor_rollout_ref.rollout.max_num_batched_tokens=8192
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:132` actor_rollout_ref.rollout.max_num_batched_tokens=$((max_prompt_length + max_response_length))
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:127` actor_rollout_ref.rollout.max_num_batched_tokens=${ROLLOUT_MAX_NUM_BATCHED_TOKENS}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
