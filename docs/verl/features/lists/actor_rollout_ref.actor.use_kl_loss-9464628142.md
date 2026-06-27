# actor_rollout_ref.actor.use_kl_loss

- **参数名**：`actor_rollout_ref.actor.use_kl_loss`
- **分类**：算法
- **中文解释**：是否在 actor loss 中加入 KL loss，用 loss 侧正则把当前策略约束在参考策略附近。
- **常见值**：$use_kl_loss、False、True
- **来源环境变量**：USE_KL_LOSS
- **性能影响**：机制推断：主要增加 loss 组合和 KL 统计开销；若所需参考 log-prob 已在流程中计算，额外成本较小。
- **精度影响**：文档说明：PPO README 说明该选项用于 KL divergence control，且使用 actor KL loss 时通常不再在 reward 中加 KL；best practices 写明 GRPO 常用 `True`，PPO/DAPO 取值不同。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：70
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:84` actor_rollout_ref.actor.use_kl_loss=False
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:67` actor_rollout_ref.actor.use_kl_loss=False
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:71` actor_rollout_ref.actor.use_kl_loss=True
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:110` actor_rollout_ref.actor.use_kl_loss=False
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:75` actor_rollout_ref.actor.use_kl_loss=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
