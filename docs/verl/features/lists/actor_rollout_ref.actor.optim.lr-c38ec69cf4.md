# actor_rollout_ref.actor.optim.lr

- **参数名**：`actor_rollout_ref.actor.optim.lr`
- **分类**：算法
- **中文解释**：Actor 策略网络优化器学习率，决定每次 PPO/GRPO 更新时参数移动幅度。
- **常见值**：$actor_lr、1.0e-05、1e-5、1e-6、3e-6、5e-7、5e-8
- **来源环境变量**：ACTOR_LR
- **性能影响**：机制推断：不显著改变单步计算量，但会影响达到目标指标所需 step 数；过高导致震荡或回滚时会浪费训练时间，过低会延长收敛。
- **精度影响**：文档说明：官方 best practices 建议从 `1e-5` 或 `1e-6` 附近开始；学习率过大易破坏策略稳定性，过小可能收敛慢或欠优化。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：79
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:80` actor_rollout_ref.actor.optim.lr=${actor_lr}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:63` actor_rollout_ref.actor.optim.lr=${actor_lr}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:67` actor_rollout_ref.actor.optim.lr=${actor_lr}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:106` actor_rollout_ref.actor.optim.lr=${ACTOR_LR}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:71` actor_rollout_ref.actor.optim.lr=${actor_lr}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
