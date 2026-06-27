# actor_rollout_ref.actor.megatron.override_transformer_config.use_distributed_optimizer

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.use_distributed_optimizer`
- **分类**：效率
- **中文解释**：文档说明：Megatron 分布式优化器开关。官方参数表列出 Actor Megatron 默认 `use_distributed_optimizer=true`；Ascend 性能文档说明大模型场景通常需要把优化器状态分片到 DP 域内每张卡上以节省显存。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：开启后可显著降低单卡优化器状态显存，支撑更大模型或 batch；代价是 optimizer step 和 checkpoint 可能增加分片通信/重分片复杂度。
- **精度影响**：机制推断：优化算法语义不变；不同分片和通信顺序可能带来微小浮点差异，配置错误则会导致状态加载或训练恢复失败。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:136` +actor_rollout_ref.actor.megatron.override_transformer_config.use_distributed_optimizer=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
