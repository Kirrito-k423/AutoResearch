# ENTROPY_COEFF

- **参数名**：`ENTROPY_COEFF`
- **分类**：算法
- **中文解释**：文档说明：对应 `actor_rollout_ref.actor.entropy_coeff`，是 PPO/RL actor loss 中熵正则项的权重，用来调节策略随机性和探索程度。
- **常见值**：0、0.0
- **来源环境变量**：ENTROPY_COEFF
- **性能影响**：机制推断：非零时需要计算并记录策略熵，主要增加少量 loss 计算和日志开销，相比 rollout/训练主体通常不是吞吐瓶颈。
- **精度影响**：文档说明：增大熵正则会鼓励更随机的策略和更多探索；过大可能削弱对高奖励输出的收敛，过小则探索不足。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：46
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:33` entropy_coeff=${ENTROPY_COEFF:-0}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:21` entropy_coeff=${ENTROPY_COEFF:-0}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:20` entropy_coeff=${ENTROPY_COEFF:-0}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:21` ENTROPY_COEFF=${ENTROPY_COEFF:-0}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:22` entropy_coeff=${ENTROPY_COEFF:-0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
