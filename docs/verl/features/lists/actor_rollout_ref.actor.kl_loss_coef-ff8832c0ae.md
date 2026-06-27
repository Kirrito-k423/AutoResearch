# actor_rollout_ref.actor.kl_loss_coef

- **参数名**：`actor_rollout_ref.actor.kl_loss_coef`
- **分类**：算法
- **中文解释**：Actor KL loss 的权重系数，控制当前策略向参考策略回拉的强度。
- **常见值**：$kl_loss_coef、0.0、0.001、0.01
- **来源环境变量**：KL_LOSS_COEF
- **性能影响**：机制推断：系数本身不改变主计算量；但较大约束可能改变收敛速度和所需训练 step，间接影响端到端耗时。
- **精度影响**：文档说明：PPO README 给出默认 0.001，best practices 建议从约 0.001 开始；更大值能抑制 reward hacking/策略漂移，但会降低探索。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：54
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`

## 证据片段

- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:72` actor_rollout_ref.actor.kl_loss_coef=${kl_loss_coef}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:96` actor_rollout_ref.actor.kl_loss_coef=0.0
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh:73` actor_rollout_ref.actor.kl_loss_coef=${kl_loss_coef}
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:71` actor_rollout_ref.actor.kl_loss_coef=${kl_loss_coef}
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:63` actor_rollout_ref.actor.kl_loss_coef=${KL_LOSS_COEF}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
