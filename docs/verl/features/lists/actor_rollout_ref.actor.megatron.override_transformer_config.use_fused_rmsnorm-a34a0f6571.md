# actor_rollout_ref.actor.megatron.override_transformer_config.use_fused_rmsnorm

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.use_fused_rmsnorm`
- **分类**：效率
- **中文解释**：文档说明：Megatron RMSNorm 融合算子开关；Ascend 性能调优文档将 `use_fused_rmsnorm=True` 列为 RMSNorm 优化配置，通常与 `normalization=RMSNorm` 配套使用。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：融合 RMSNorm 可减少归一化计算的 kernel launch 和访存开销，在 NPU/Megatron 训练中用于提升吞吐。
- **精度影响**：机制推断：与普通 RMSNorm 目标等价；融合低精度 kernel 可能带来微小舍入差异，若模型不是 RMSNorm 或后端不支持则不应启用。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:133` +actor_rollout_ref.actor.megatron.override_transformer_config.use_fused_rmsnorm=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
