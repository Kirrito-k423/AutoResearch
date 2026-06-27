# actor_rollout_ref.actor.ppo_mini_batch_size

- **参数名**：`actor_rollout_ref.actor.ppo_mini_batch_size`
- **分类**：效率
- **中文解释**：控制 PPO/反向传播分块大小，是显存占用和 step 时间的核心旋钮。
- **常见值**：$ppo_mini_batch_size、1024、128、16、256、3、32、4、512、64、8
- **来源环境变量**：PPO_MINI_BATCH_SIZE、ppo_mini_batch_size
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:81` actor_rollout_ref.actor.ppo_mini_batch_size=${ppo_mini_batch_size}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:64` actor_rollout_ref.actor.ppo_mini_batch_size=${ppo_mini_batch_size}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:68` actor_rollout_ref.actor.ppo_mini_batch_size=${ppo_mini_batch_size}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:107` actor_rollout_ref.actor.ppo_mini_batch_size=${ppo_mini_batch_size}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:72` actor_rollout_ref.actor.ppo_mini_batch_size=${ppo_mini_batch_size}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
