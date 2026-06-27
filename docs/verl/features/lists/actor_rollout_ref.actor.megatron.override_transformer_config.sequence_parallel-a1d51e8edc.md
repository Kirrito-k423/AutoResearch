# actor_rollout_ref.actor.megatron.override_transformer_config.sequence_parallel

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.sequence_parallel`
- **分类**：效率
- **中文解释**：文档说明：Megatron Transformer 覆盖配置中的 sequence parallel 开关；Ascend 性能文档说明 SP 在 Tensor Parallel 基础上沿序列维度进一步切分输入，用于降低长序列激活压力并提高计算效率。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：开启 SP 可在长序列/大模型场景下降低单卡激活显存，并配合 TP 改善吞吐；代价是额外的序列维通信和对并行拓扑的约束。
- **精度影响**：机制推断：不改变训练目标；跨 rank 切分与聚合会改变浮点归约顺序，可能有微小数值差异。SP/TP 配置不一致时更可能表现为 shape 或通信错误。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:137` +actor_rollout_ref.actor.megatron.override_transformer_config.sequence_parallel=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
