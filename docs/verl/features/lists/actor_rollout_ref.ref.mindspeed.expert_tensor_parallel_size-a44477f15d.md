# actor_rollout_ref.ref.mindspeed.expert_tensor_parallel_size

- **参数名**：`actor_rollout_ref.ref.mindspeed.expert_tensor_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Reference MindSpeed/Megatron MoE 的专家张量并行 ETP 大小，用于在专家内部再做 tensor parallel；示例常见值为 1。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：文档说明：EP/ETP 属于 Megatron 并行参数，需要按显存和网络约束平衡；ETP 增大可降低单卡专家矩阵显存/计算压力，但会增加专家内部 tensor-parallel 通信。
- **精度影响**：机制推断：正确切分时不改变 ref 计算；ETP 与 checkpoint、TP/EP 或 actor 配置不一致会导致权重形状和 KL/reference 结果错误。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:161` actor_rollout_ref.ref.mindspeed.expert_tensor_parallel_size=${train_etp}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
