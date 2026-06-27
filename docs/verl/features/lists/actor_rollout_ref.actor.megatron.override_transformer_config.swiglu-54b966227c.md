# actor_rollout_ref.actor.megatron.override_transformer_config.swiglu

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.swiglu`
- **分类**：效率
- **中文解释**：机制推断：覆盖 Megatron Transformer 的 MLP 激活结构为 SwiGLU。Qwen 系列等模型通常使用 SwiGLU，示例在 NPU/Megatron 脚本中与 `use_fused_swiglu=True` 配套设置，用于保证训练侧结构与预训练模型一致并启用相应优化路径。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：SwiGLU 本身是模型结构选择；配合 fused SwiGLU/NPU 优化内核时可降低激活计算开销。单独打开但无融合 kernel 时未必带来性能收益。
- **精度影响**：机制推断：这是结构匹配参数，不是可随意调的数值优化项；若与 checkpoint 的 MLP 激活不一致，会改变模型函数并严重影响训练/加载正确性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:134` +actor_rollout_ref.actor.megatron.override_transformer_config.swiglu=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
