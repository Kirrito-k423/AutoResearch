# actor_rollout_ref.rollout.top_k

- **参数名**：`actor_rollout_ref.rollout.top_k`
- **分类**：算法
- **中文解释**：文档说明：rollout Top-K 采样参数，官方参数表写明 `-1` 表示不启用；官方最佳实践将它与 temperature/top_p 并列为 rollout 采样旋钮。
- **常见值**：-1、50
- **来源环境变量**：TOP_K
- **性能影响**：机制推断：主要影响采样后处理候选集，对模型前向成本影响小；小 K 可能略减少采样开销，但端到端收益通常不如 batch/并行参数显著。
- **精度影响**：文档说明：官方建议 rollout 可用 `top_k=-1` 保持足够随机性，验证也可从 `top_k=-1` 起步；较小 K 会降低多样性并可能减少探索。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:128` actor_rollout_ref.rollout.top_k=${top_k}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:139` actor_rollout_ref.rollout.top_k=-1
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:163` actor_rollout_ref.rollout.top_k=${top_k}
- `examples/generation/run_deepseek_llm_7b.sh:38` actor_rollout_ref.rollout.top_k=50 \
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:165` actor_rollout_ref.rollout.top_k=-1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
