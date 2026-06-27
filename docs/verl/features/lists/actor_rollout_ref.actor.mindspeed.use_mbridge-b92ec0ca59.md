# actor_rollout_ref.actor.mindspeed.use_mbridge

- **参数名**：`actor_rollout_ref.actor.mindspeed.use_mbridge`
- **分类**：效率
- **中文解释**：文档说明：为 MindSpeed actor 启用 mBridge/Megatron-Bridge 权重桥接与格式转换，使 HuggingFace/Megatron 权重能按 MindSpeed Megatron 并行配置加载和同步。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：mBridge 主要影响启动、checkpoint 转换和训练-推理权重同步链路；会增加转换/IO 开销，但能避免格式不匹配造成的运行失败。
- **精度影响**：机制推断：正确桥接后不改变训练目标；若桥接路径或并行配置不一致，可能导致权重切分错误、logprob/KL 口径异常或加载失败。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:125` actor_rollout_ref.actor.mindspeed.use_mbridge=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:130` actor_rollout_ref.actor.mindspeed.use_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
