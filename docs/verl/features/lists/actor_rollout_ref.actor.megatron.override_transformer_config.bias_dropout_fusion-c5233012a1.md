# actor_rollout_ref.actor.megatron.override_transformer_config.bias_dropout_fusion

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.bias_dropout_fusion`
- **分类**：效率
- **中文解释**：机制推断：Megatron Transformer 覆盖配置中的 bias/dropout 融合开关，用融合 kernel 合并 bias、dropout 及残差相关小算子；Verl 的 MCore 配置转换器在多种模型配置里默认打开该优化。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：融合后可减少 kernel launch、读写显存次数和中间张量，通常提升训练吞吐；收益依赖 Megatron/MCore、Transformer Engine 和硬件后端是否支持。
- **精度影响**：机制推断：数学目标不变；融合实现可能改变 dropout 随机数消费顺序或浮点舍入顺序，通常只带来可接受的微小数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:163` +actor_rollout_ref.actor.megatron.override_transformer_config.bias_dropout_fusion=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
