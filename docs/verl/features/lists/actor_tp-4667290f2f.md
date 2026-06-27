# actor_tp

- **参数名**：`actor_tp`
- **分类**：效率
- **中文解释**：机制推断：示例脚本中的 actor tensor parallel 环境变量，通常写入 actor/ref Megatron `tensor_model_parallel_size`，控制 actor 训练和 ref 前向的张量并行切分度。
- **常见值**：1
- **来源环境变量**：actor_tp
- **性能影响**：机制推断：TP 增大可降低单卡权重/激活压力并支持更大模型，但会增加层内通信和并行调度开销；TP 太小易 OOM，太大可能吞吐下降。
- **精度影响**：机制推断：正确张量并行不改变优化目标；若 actor、ref、checkpoint 或 rollout 相关并行度不匹配，可能导致加载失败或 logprob 数值一致性风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:52` actor_tp=${actor_tp:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
