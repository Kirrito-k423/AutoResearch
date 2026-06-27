# actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion`
- **分类**：效率
- **中文解释**：文档说明：Megatron MoE transformer override 中的 token permutation fusion 开关；官方最佳实践把它列为 MoE 性能推荐 knob 之一。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：作为 MoE recommended knob，用于融合或优化专家 token permute 相关操作；开启目标是降低 MoE 调度/拷贝开销，具体收益依赖模型和硬件。
- **精度影响**：机制推断：应是等价融合优化，不改变路由目标；若后端/kernel 不兼容，风险主要是数值差异或运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:95` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:86` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion=True
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:117` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion=True
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:90` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion=True
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:136` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_permute_fusion=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
