# actor_rollout_ref.actor.megatron.override_transformer_config.use_naive_l2norm

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.use_naive_l2norm`
- **分类**：效率
- **中文解释**：机制推断：Megatron Transformer 覆盖配置中的 L2Norm 实现选择开关。Verl 本地 docs/源码和官方公开搜索未找到独立参数说明，只在 Qwen3.5-35B Megatron 示例中出现；按命名理解，它用于让模型中的 L2Norm/QK-norm 类归一化路径使用朴素实现而非特化融合实现。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：朴素 L2Norm 通常优先兼容性和数值可解释性，可能比特化/融合实现慢，尤其在长序列或高维 hidden states 下会增加 kernel 与访存开销。
- **精度影响**：机制推断：归一化公式应保持一致，但朴素实现与融合实现可能有不同的舍入和 epsilon 处理；对依赖 QK/L2Norm 的模型，应按官方示例保持该开关以避免实现不匹配。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:200` +actor_rollout_ref.actor.megatron.override_transformer_config.use_naive_l2norm=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
