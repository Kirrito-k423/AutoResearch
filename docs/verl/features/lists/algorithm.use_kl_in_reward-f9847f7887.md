# algorithm.use_kl_in_reward

- **参数名**：`algorithm.use_kl_in_reward`
- **分类**：算法
- **中文解释**：是否把相对参考模型的 KL 惩罚加入 reward，用 reward 侧约束策略不要偏离参考策略太远。
- **常见值**：$use_kl_in_reward、False、True
- **来源环境变量**：USE_KL_IN_REWARD
- **性能影响**：机制推断：启用后需要 KL 相关计算和记录，通常小于 rollout/训练主耗时；若引入参考 log-prob 计算路径，会增加少量前向开销。
- **精度影响**：文档说明：best practices 写明 PPO 常用 `True`，GRPO/DAPO 常用 `False`；启用后强化对参考模型的约束，可降低漂移和 reward hacking，但可能压制探索。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：72
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
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:58` algorithm.use_kl_in_reward=False
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:46` algorithm.use_kl_in_reward=True
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:47` algorithm.use_kl_in_reward=False
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:84` algorithm.use_kl_in_reward=False
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:50` algorithm.use_kl_in_reward=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
