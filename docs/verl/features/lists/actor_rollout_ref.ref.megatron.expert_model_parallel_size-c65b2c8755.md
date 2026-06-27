# actor_rollout_ref.ref.megatron.expert_model_parallel_size

- **参数名**：`actor_rollout_ref.ref.megatron.expert_model_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Megatron reference policy 的 MoE expert model parallel 并行度，决定 ref 模型专家层按 EP 维度切分；官方建议 ref 的 Megatron 并行参数与 actor 保持同步。
- **常见值**：${actor_ep、16、4、8
- **来源环境变量**：ACTOR_EP、EP、REF_EP
- **性能影响**：文档说明：官方最佳实践要求 PP/TP/EP/ETP/CP 根据显存和网络约束平衡；增大 EP 可分摊 MoE 专家参数和计算压力，但会增加专家通信与调度开销。
- **精度影响**：机制推断：正确的 expert parallel 是等价切分，通常不直接改变 reference logprob/KL；若与 actor 或 checkpoint 权重布局不一致，可能导致加载、同步或 ref logprob 对齐问题。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：12
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:115` actor_rollout_ref.ref.megatron.expert_model_parallel_size=${actor_ep}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:110` actor_rollout_ref.ref.megatron.expert_model_parallel_size=${actor_ep}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:152` actor_rollout_ref.ref.megatron.expert_model_parallel_size=${actor_ep}
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:86` actor_rollout_ref.ref.megatron.expert_model_parallel_size=${ACTOR_EP}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:163` actor_rollout_ref.ref.megatron.expert_model_parallel_size=${EP}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
