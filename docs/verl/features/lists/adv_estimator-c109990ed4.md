# adv_estimator

- **参数名**：`adv_estimator`
- **分类**：算法
- **中文解释**：examples 暴露的优势估计器变量，最终写入 `algorithm.adv_estimator`；用于选择把 reward/价值信号转换为策略梯度 advantage 的算法，当前示例默认 `grpo`。
- **常见值**：grpo
- **来源环境变量**：adv_estimator
- **性能影响**：机制推断：估计器本身通常不是主要吞吐瓶颈，但不同 estimator 可能改变是否需要 critic、baseline、分组统计或额外归一化，从而影响训练开销和显存。
- **精度影响**：文档说明：Verl PPO/GRPO 文档列出 `algorithm.adv_estimator` 支持 `gae`、`grpo`、`reinforce_plus_plus`、`rloo` 等；该选择直接改变优势信号的 bias/variance 和训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:55` adv_estimator=${adv_estimator:-grpo}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
