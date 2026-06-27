# actor_rollout_ref.actor.entropy_from_logits_with_chunking

- **参数名**：`actor_rollout_ref.actor.entropy_from_logits_with_chunking`
- **分类**：算法
- **中文解释**：文档说明：让 actor 在从 logits 计算熵时按 chunk 分块处理，而不是一次性处理完整 `[bsz*seq_len, vocab]` 张量；用于降低训练前向中熵计算的显存峰值。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：显著降低熵计算的峰值显存，尤其适合长序列/大词表；机制推断：分块循环可能带来少量额外 kernel/调度开销，但常换来更大的 batch 或避免 OOM。
- **精度影响**：机制推断：目标仍是同一个 logits 熵，理论上不改变 RL 目标；实际只可能因分块顺序和浮点舍入带来极小数值差异，主要收益是稳定跑完大模型/长上下文。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:153` actor_rollout_ref.actor.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:103` actor_rollout_ref.actor.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:90` actor_rollout_ref.actor.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:115` actor_rollout_ref.actor.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:90` actor_rollout_ref.actor.entropy_from_logits_with_chunking=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
