# actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu

- **参数名**：`actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu`
- **分类**：效率
- **中文解释**：动态 batch 模式下，rollout/old policy 计算 log-prob 前向时单 GPU 允许处理的最大 token 数。
- **常见值**：$(((max_prompt_length + max_response_length) * 1))、$(((max_prompt_length + max_response_length) * 2))、$(((max_prompt_length + max_response_length) * 3))、$(((max_prompt_length + max_response_length) / sp_size))、$(((max_prompt_length + max_response_length))、$((MAX_PROMPT_LENGTH + MAX_RESPONSE_LENGTH))、$((max_prompt_length + max_response_length))、10240、12288、20480、24576、30720
- **来源环境变量**：PPO_MAX_TOKEN_LEN_PER_GPU、ROLLOUT_LOG_PROB_MAX_TOKEN_LEN_PER_GPU、ppo_max_token_len_per_gpu
- **性能影响**：文档说明：best practices 要求至少设为 `max_prompt_length + max_response_length` 的倍数以避免截断；perf tuning 将其定义为 `compute_log_prob` 前向的最大 token 数。
- **精度影响**：机制推断：不改变 log-prob 数学定义；设置过低会导致分批过碎或无法覆盖长序列，间接影响训练效率和稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：60
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:107` actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=${ppo_max_token_len_per_gpu}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:79` actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=${ppo_max_token_len_per_gpu}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:85` actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=${ppo_max_token_len_per_gpu}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:122` actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=${PPO_MAX_TOKEN_LEN_PER_GPU}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:99` actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=${ppo_max_token_len_per_gpu}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
