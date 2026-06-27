# actor_rollout_ref.actor.checkpoint.strict

- **参数名**：`actor_rollout_ref.actor.checkpoint.strict`
- **分类**：效率
- **中文解释**：文档说明：Actor checkpoint 配置里的严格校验开关，Verl 默认注释为“权重导出时是否执行严格验证”。示例设为 `False`，通常用于允许 Megatron/LoRA/模型转换场景中存在非完全匹配的权重键。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：严格校验本身主要影响 checkpoint 导出/加载阶段的检查与失败行为，通常不影响训练吞吐；关闭严格模式可减少因键不完全匹配导致的中断，但不能降低实际保存 IO。
- **精度影响**：机制推断：训练中不直接改变数值；但关闭严格校验可能掩盖缺失或未预期权重，若模型转换确实不完整，会影响恢复后模型质量或可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:197` actor_rollout_ref.actor.checkpoint.strict=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
