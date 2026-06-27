# actor_rollout_ref.ref.entropy_from_logits_with_chunking

- **参数名**：`actor_rollout_ref.ref.entropy_from_logits_with_chunking`
- **分类**：算法
- **中文解释**：文档说明：让 reference model 在从 logits 计算熵时使用分块计算，避免一次性处理完整 `[bsz*seq_len, vocab]` 张量导致显存峰值过高。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：降低 ref 前向相关熵计算的峰值显存，适合长序列/大词表；机制推断：可能增加少量分块循环开销，但可避免 OOM 或支持更大 batch。
- **精度影响**：机制推断：分块计算的是同一熵表达式，通常不改变参考策略语义；只可能存在极小浮点舍入差异，若 ref 权重正确则对 KL/约束目标影响很小。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:148` actor_rollout_ref.ref.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:102` actor_rollout_ref.ref.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:144` actor_rollout_ref.ref.entropy_from_logits_with_chunking=True
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:102` actor_rollout_ref.ref.entropy_from_logits_with_chunking=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:130` actor_rollout_ref.ref.entropy_from_logits_with_chunking=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
