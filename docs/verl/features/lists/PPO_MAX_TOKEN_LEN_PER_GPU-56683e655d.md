# PPO_MAX_TOKEN_LEN_PER_GPU

- **参数名**：`PPO_MAX_TOKEN_LEN_PER_GPU`
- **分类**：效率
- **中文解释**：文档说明：对应 actor/ref/critic 动态 batch 的每 GPU token 上限，限制一次 forward/backward 或 log-prob 计算可处理的 token 数，常按 `max_prompt_length + max_response_length` 的倍数设置以避免 OOM 并提升吞吐。
- **常见值**：$((MAX_PROMPT_LENGTH + MAX_RESPONSE_LENGTH))、$((max_prompt_length + max_response_length))、10240、12288、20480、24576、30720、32768、4096、8192
- **来源环境变量**：PPO_MAX_TOKEN_LEN_PER_GPU
- **性能影响**：文档说明：这是本地 per-GPU 性能参数；调大可提高动态 batch 吞吐，但会增加激活/显存峰值，长序列训练时需要下调以避免 OOM。
- **精度影响**：机制推断：通常不改变优化目标；若设置过小导致样本被截断、频繁 OOM 或有效 batch 下降，可能间接影响训练稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：47
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:30` ppo_max_token_len_per_gpu=${PPO_MAX_TOKEN_LEN_PER_GPU:-30720}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:18` ppo_max_token_len_per_gpu=${PPO_MAX_TOKEN_LEN_PER_GPU:-24576}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:16` ppo_max_token_len_per_gpu=${PPO_MAX_TOKEN_LEN_PER_GPU:-24576}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:18` PPO_MAX_TOKEN_LEN_PER_GPU=${PPO_MAX_TOKEN_LEN_PER_GPU:-20480}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:19` ppo_max_token_len_per_gpu=${PPO_MAX_TOKEN_LEN_PER_GPU:-30720}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
