# actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion`
- **分类**：效率
- **中文解释**：文档说明：向 Megatron Transformer 配置注入梯度累积融合开关；Verl best practices 明确说明它用于启用 fused gradient accumulation。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：启用融合梯度累积可获得额外加速，通常减少梯度累积阶段的 kernel/内存访问开销。
- **精度影响**：机制推断：不改变损失定义；融合会改变部分累积顺序和 kernel 数值路径，可能带来极小浮点差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:121` +actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion=True
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:89` +actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:164` +actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion=True
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:59` ++actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion=False
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:112` +actor_rollout_ref.actor.megatron.override_transformer_config.gradient_accumulation_fusion=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
