# actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype`
- **分类**：效率
- **中文解释**：文档说明：覆盖 Megatron Transformer 中 MoE router 与专家输出加权平均的数据类型；Ascend/Verl 文档列出 `fp32`/`fp64`，默认常用 `fp32`，用于提升多专家场景稳定性。
- **常见值**：fp32
- **来源环境变量**：无
- **性能影响**：机制推断：使用 fp32/fp64 router 会比低精度路由略增计算和带宽开销，但可减少路由数值问题带来的性能抖动或失败。
- **精度影响**：文档说明：更高精度的 router dtype 可提高 MoE 路由和专家加权稳定性，尤其专家数量较多时有利于训练稳定。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:94` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype=fp32
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:85` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype=fp32
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:113` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype=fp32
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:117` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype=fp32
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:83` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_router_dtype=fp32

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
