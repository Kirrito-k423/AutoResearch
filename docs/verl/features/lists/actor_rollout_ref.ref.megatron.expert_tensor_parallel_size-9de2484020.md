# actor_rollout_ref.ref.megatron.expert_tensor_parallel_size

- **参数名**：`actor_rollout_ref.ref.megatron.expert_tensor_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Megatron reference policy 的 MoE expert tensor parallel 并行度，控制单个 expert 内部张量切分；官方建议 ref 并行参数与 actor 保持同步。
- **常见值**：1、4
- **来源环境变量**：ACTOR_ETP、ETP
- **性能影响**：文档说明：EP/ETP/TP/PP/CP 需要按显存与网络约束平衡；增大 ETP 可降低单卡 expert 权重或激活压力，但可能增加专家内部通信。
- **精度影响**：机制推断：正确 ETP 是等价张量切分，通常不直接改变 reference 输出；不匹配可能导致权重加载或 logprob 对齐问题。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：10
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:116` actor_rollout_ref.ref.megatron.expert_tensor_parallel_size=${actor_etp}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:111` actor_rollout_ref.ref.megatron.expert_tensor_parallel_size=${actor_etp}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:153` actor_rollout_ref.ref.megatron.expert_tensor_parallel_size=${actor_etp}
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:87` actor_rollout_ref.ref.megatron.expert_tensor_parallel_size=${ACTOR_ETP}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:164` actor_rollout_ref.ref.megatron.expert_tensor_parallel_size=${ETP}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
