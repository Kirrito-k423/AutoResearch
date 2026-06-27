# ROLLOUT_EP

- **参数名**：`ROLLOUT_EP`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧 MoE expert parallel size，示例写入 `actor_rollout_ref.rollout.expert_parallel_size`，用于控制推理引擎中的专家并行切分。
- **常见值**：64
- **来源环境变量**：ROLLOUT_EP
- **性能影响**：机制推断：增大 EP 可分摊 MoE expert 权重和计算，支撑更大模型或更高并发，但会增加专家路由通信与调度复杂度。
- **精度影响**：机制推断：正确 expert 并行应保持输出等价；并行/路由实现不兼容可能带来同步或数值差异，通常不是主动调精度的参数。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:35` ROLLOUT_EP=${ROLLOUT_EP:-64}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
