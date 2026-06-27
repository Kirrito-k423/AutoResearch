# actor_rollout_ref.model.use_remove_padding

- **参数名**：`actor_rollout_ref.model.use_remove_padding`
- **分类**：效率
- **中文解释**：启用 remove padding/sequence packing，在支持的模型上去掉 padding token 的无效计算。
- **常见值**：$use_remove_padding、False、True
- **来源环境变量**：无
- **性能影响**：文档说明：官方 perf tuning 建议启用 `use_remove_padding=True` 做 sequence packing；对 llama、mistral、gemma1、qwen 等模型可减少 padding 计算并提升有效吞吐。
- **精度影响**：机制推断：理论上不改变非 padding token 的训练目标；但模型/后端不支持或与其他特性不兼容时，可能导致数值或运行稳定性问题。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：64
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
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:71` actor_rollout_ref.model.use_remove_padding=True
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:58` actor_rollout_ref.model.use_remove_padding=True
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:59` actor_rollout_ref.model.use_remove_padding=True
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:96` actor_rollout_ref.model.use_remove_padding=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:62` actor_rollout_ref.model.use_remove_padding=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
