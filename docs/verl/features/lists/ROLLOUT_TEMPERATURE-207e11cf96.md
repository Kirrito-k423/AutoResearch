# ROLLOUT_TEMPERATURE

- **参数名**：`ROLLOUT_TEMPERATURE`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.temperature`，控制训练 rollout 的采样温度；官方最佳实践将它与 `top_p`、`top_k` 一起列为 rollout 采样旋钮。
- **常见值**：1.0
- **来源环境变量**：ROLLOUT_TEMPERATURE
- **性能影响**：机制推断：温度缩放本身计算开销很小；它可能通过 EOS 概率、输出长度和重采样分布轻微影响端到端 rollout 耗时。
- **精度影响**：文档说明：官方建议 rollout 保持足够随机性；temperature 越高探索越强、方差越大，越低越接近贪心采样。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:60` rollout_temperature=${ROLLOUT_TEMPERATURE:-1.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
