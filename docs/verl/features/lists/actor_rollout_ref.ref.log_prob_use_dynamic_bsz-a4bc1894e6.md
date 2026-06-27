# actor_rollout_ref.ref.log_prob_use_dynamic_bsz

- **参数名**：`actor_rollout_ref.ref.log_prob_use_dynamic_bsz`
- **分类**：效率
- **中文解释**：在 reference policy 计算参考 log-prob 时启用动态 batch，让分批按 token 预算适配不同序列长度。
- **常见值**：False、True
- **来源环境变量**：USE_DYNAMIC_BSZ
- **性能影响**：文档说明：best practices 推荐为 reference policy 启用动态 batching；perf tuning 说明动态 batch 能提升效率并降低显存压力。
- **精度影响**：机制推断：只改变参考模型前向的批处理组织，不改变 KL/log-prob 定义；仅在 token 上限或显存配置不当时产生间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：55
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
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:111` actor_rollout_ref.ref.log_prob_use_dynamic_bsz=True
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:83` actor_rollout_ref.ref.log_prob_use_dynamic_bsz=True
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:89` actor_rollout_ref.ref.log_prob_use_dynamic_bsz=True
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:126` actor_rollout_ref.ref.log_prob_use_dynamic_bsz=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:106` actor_rollout_ref.ref.log_prob_use_dynamic_bsz=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
