# actor_rollout_ref.actor.mindspeed.expert_tensor_parallel_size

- **参数名**：`actor_rollout_ref.actor.mindspeed.expert_tensor_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：MindSpeed/Megatron Actor 的专家张量并行（ETP）大小，用于 MoE 专家内部或专家相关矩阵的 TP 切分；Verl dataclass 注释说明该字段是 MoE models 的 expert tensor parallel size。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：文档说明：ETP 可进一步分摊单个专家的参数和计算，缓解大专家显存压力；但会增加专家内部通信，专家较小时过度切分可能得不偿失。
- **精度影响**：机制推断：不改变 MoE 训练目标；仅改变专家权重和计算的分布式切分。错误的 ETP/EP/TP 组合可能导致 shape、通信或 checkpoint 兼容问题。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:124` actor_rollout_ref.actor.mindspeed.expert_tensor_parallel_size=${train_etp}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
