# GEN_MOE_EP

- **参数名**：`GEN_MOE_EP`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧 MoE expert parallel 大小，示例把 `GEN_MOE_EP` 写入 `actor_rollout_ref.rollout.expert_parallel_size`，用于控制专家并行切分。
- **常见值**：2
- **来源环境变量**：GEN_MOE_EP
- **性能影响**：机制推断：增大 EP 可分摊 MoE expert 权重和计算、支撑更大 MoE rollout，但会增加专家路由通信、调度复杂度和后端兼容要求。
- **精度影响**：机制推断：正确 expert parallel 应保持推理输出等价；若与 TP、MoE tensor parallel 或 checkpoint/后端支持不匹配，可能导致加载失败、路由不一致或数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:55` gen_moe_ep=${GEN_MOE_EP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
