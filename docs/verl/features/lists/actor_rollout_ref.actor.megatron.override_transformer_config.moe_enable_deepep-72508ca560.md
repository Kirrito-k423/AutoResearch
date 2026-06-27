# actor_rollout_ref.actor.megatron.override_transformer_config.moe_enable_deepep

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_enable_deepep`
- **分类**：效率
- **中文解释**：文档说明：该 Megatron `override_transformer_config` 开关用于 MoE 模型启用 DeepEP 相关通信/dispatcher 优化；Verl 性能建议把 `moe_enable_deepep=True` 列为推荐的 MoE 稳定性能旋钮之一。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：DeepEP 面向 MoE 专家并行 all-to-all/dispatcher 通信优化，可能提升 MoE token dispatch 吞吐；实际效果依赖 DeepEP 安装、GPU/NPU 平台和 EP/ETP 拓扑。
- **精度影响**：机制推断：不改变模型目标或 reward；可能因不同 dispatcher/kernel 的浮点顺序产生微小数值差异，主要风险是平台兼容性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:115` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_enable_deepep=True
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:84` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_enable_deepep=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:107` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_enable_deepep=True
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:112` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_enable_deepep=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
