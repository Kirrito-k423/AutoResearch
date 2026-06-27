# actor_rollout_ref.actor.megatron.override_transformer_config.normalization

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.normalization`
- **分类**：效率
- **中文解释**：机制推断：覆盖 Megatron Transformer 的归一化层类型，示例设为 `RMSNorm`，用于让 Megatron 构造出的模型结构与 Qwen 等采用 RMSNorm 的预训练模型配置一致。
- **常见值**：RMSNorm
- **来源环境变量**：无
- **性能影响**：机制推断：RMSNorm 通常比 LayerNorm 少均值相关计算，且可配合 fused RMSNorm kernel 提升吞吐；但主要作用是匹配模型结构，而不是单纯性能开关。
- **精度影响**：机制推断：这是模型结构参数，必须与 checkpoint/配置一致；错误的 normalization 类型会改变网络函数，导致权重加载不匹配或训练/评测质量严重异常。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:132` +actor_rollout_ref.actor.megatron.override_transformer_config.normalization=RMSNorm

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
