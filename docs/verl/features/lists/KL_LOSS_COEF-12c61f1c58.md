# KL_LOSS_COEF

- **参数名**：`KL_LOSS_COEF`
- **分类**：算法
- **中文解释**：文档说明：对应 `actor_rollout_ref.actor.kl_loss_coef`，是在 actor loss 中加入 KL loss 时使用的权重，用于约束当前策略不要过度偏离参考策略。
- **常见值**：0.001、0.01
- **来源环境变量**：KL_LOSS_COEF
- **性能影响**：机制推断：主要增加 KL loss 聚合/反传中的少量计算；真正的额外开销通常来自是否需要 reference log-prob，而不是系数本身。
- **精度影响**：文档说明：较大系数会抑制 reward hacking、降低策略漂移但减少探索；过小可能让策略更快偏离参考模型，稳定性风险上升。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：32
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`

## 证据片段

- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:19` kl_loss_coef=${KL_LOSS_COEF:-0.001}
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh:19` kl_loss_coef=${KL_LOSS_COEF:-0.001}
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:25` kl_loss_coef=${KL_LOSS_COEF:-0.01}
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:20` KL_LOSS_COEF=${KL_LOSS_COEF:-0.001}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:23` kl_loss_coef=${KL_LOSS_COEF:-0.001}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
