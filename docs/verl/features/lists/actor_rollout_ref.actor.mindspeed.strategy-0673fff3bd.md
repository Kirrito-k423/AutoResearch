# actor_rollout_ref.actor.mindspeed.strategy

- **参数名**：`actor_rollout_ref.actor.mindspeed.strategy`
- **分类**：效率
- **中文解释**：文档说明：选择 MindSpeed actor 的训练策略，示例使用 `mindspeed_megatron`。Verl engine workers 文档把 NPU 上的 `mindspeed_megatron` 映射到 MindSpeed Megatron engine。
- **常见值**：mindspeed_megatron
- **来源环境变量**：无
- **性能影响**：文档说明：该策略决定训练后端、并行组织和 NPU/MindSpeed 优化路径；切到 MindSpeed Megatron 会影响显存切分、通信模式和可用 fused kernel。
- **精度影响**：机制推断：训练目标不变，但不同后端的精度类型、融合算子和通信归约顺序可能带来细微数值差异；配置不匹配会导致权重加载或并行对齐失败。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:128` actor_rollout_ref.actor.mindspeed.strategy=mindspeed_megatron
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:133` actor_rollout_ref.actor.mindspeed.strategy=mindspeed_megatron

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
