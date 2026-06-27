# actor_rollout_ref.rollout.dtype

- **参数名**：`actor_rollout_ref.rollout.dtype`
- **分类**：效率
- **中文解释**：指定 rollout 推理后端加载模型权重和执行推理时使用的数据类型，示例中常用 `bfloat16`。
- **常见值**："bfloat16"、bfloat16
- **来源环境变量**：无
- **性能影响**：文档说明：vLLM 官方参数中 `dtype` 控制权重和激活精度；BF16/FP16 通常减少显存与带宽压力、提高吞吐，FP32 更耗显存和算力。
- **精度影响**：机制推断：低精度推理可能带来轻微数值差异；BF16 具有较宽指数范围，通常比 FP16 更稳，但仍可能影响采样边界和 logprob。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:90` actor_rollout_ref.rollout.dtype=${dtype}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:149` actor_rollout_ref.rollout.dtype=bfloat16
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:118` actor_rollout_ref.rollout.dtype=bfloat16

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
