# actor_rollout_ref.actor.megatron.override_transformer_config.bias_activation_fusion

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.bias_activation_fusion`
- **分类**：效率
- **中文解释**：文档说明：覆盖 Megatron transformer config 中 bias 与 activation 融合开关；Ascend 迁移文档提到 `bias_activation_fusion=True` 可让训练侧进入 NPU 融合算子分支，避免与推理侧融合实现不一致。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：融合 bias 和激活可减少算子启动与中间张量读写，在 NPU/Megatron 路径上通常提升 FFN/SwiGLU 类模块执行效率。
- **精度影响**：文档说明：目标上应保持等价，但融合实现会改变浮点执行路径；Ascend 迁移文档把该开关列为修复训推不一致的关键配置，错误配置可能带来数值对齐问题。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:162` +actor_rollout_ref.actor.megatron.override_transformer_config.bias_activation_fusion=True
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:115` +actor_rollout_ref.actor.megatron.override_transformer_config.bias_activation_fusion=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
