# CLIP_RATIO

- **参数名**：`CLIP_RATIO`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，用作 actor clip ratio 的通用默认值，常被脚本同时填入 `clip_ratio_low` 和 `clip_ratio_high`，表示 PPO 类目标的 policy ratio 裁剪范围。
- **常见值**：0.4
- **来源环境变量**：CLIP_RATIO
- **性能影响**：机制推断：只改变 loss 裁剪阈值，额外计算开销可忽略；主要影响训练稳定性和收敛过程。
- **精度影响**：文档说明：裁剪范围越窄，策略更新越保守、稳定性通常更好但学习可能变慢；范围越宽，优化自由度更大但更易出现过大更新。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:22` clip_ratio=${CLIP_RATIO:-0.4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
