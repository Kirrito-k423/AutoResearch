# actor_rollout_ref.actor.use_dynamic_bsz

- **参数名**：`actor_rollout_ref.actor.use_dynamic_bsz`
- **分类**：效率
- **中文解释**：为 actor 更新启用动态 batch size，使每次前向/反向尽量处理相近 token 数，而不是固定样本数。
- **常见值**：$use_dynamic_bsz、False、True
- **来源环境变量**：USE_DYNAMIC_BSZ
- **性能影响**：文档说明：官方 perf tuning 说明动态 batch 能显著提升训练效率并降低显存占用；启用后重点调 `ppo_max_token_len_per_gpu`，不再主要调 micro batch。
- **精度影响**：机制推断：目标函数不变，通常不直接影响精度；但 token 上限过小会导致 batch 切分过细或无法覆盖长序列，间接影响稳定性与吞吐。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：64
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
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:82` actor_rollout_ref.actor.use_dynamic_bsz=True
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:65` actor_rollout_ref.actor.use_dynamic_bsz=True
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:69` actor_rollout_ref.actor.use_dynamic_bsz=True
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:108` actor_rollout_ref.actor.use_dynamic_bsz=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:73` actor_rollout_ref.actor.use_dynamic_bsz=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
