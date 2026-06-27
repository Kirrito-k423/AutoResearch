# actor_rollout_ref.actor.megatron.override_transformer_config.persist_layer_norm

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.persist_layer_norm`
- **分类**：效率
- **中文解释**：文档说明：Megatron LayerNorm/RMSNorm 执行优化开关；Ascend 高级特性文档说明 `persist_layer_norm` 表示使用持久化策略优化 LayerNorm，默认值为 `False`。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：持久化 LayerNorm 属于训练侧 Megatron 融合/优化项，可减少归一化相关访存和 kernel 开销；收益依赖隐藏维度、后端 kernel 支持和硬件。
- **精度影响**：机制推断：目标上与普通 LayerNorm/RMSNorm 等价；低精度融合实现会改变舍入路径，通常只产生微小数值差异，若 kernel 不支持则应回退或失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:166` +actor_rollout_ref.actor.megatron.override_transformer_config.persist_layer_norm=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
