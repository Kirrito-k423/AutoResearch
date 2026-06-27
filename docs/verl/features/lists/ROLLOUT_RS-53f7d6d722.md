# ROLLOUT_RS

- **参数名**：`ROLLOUT_RS`
- **分类**：效率
- **中文解释**：控制 `algorithm.rollout_correction.rollout_rs`，即 Rollout Correction 的 rejection sampling 模式；示例默认 `token_k1`，表示按 token 级 `-log r` 比率边界过滤 rollout 与训练策略偏差过大的 token/样本。
- **常见值**：token_k1
- **来源环境变量**：ROLLOUT_RS
- **性能影响**：文档说明：启用 RS 后需要计算校正权重/拒绝 mask，并可能减少参与 loss 的有效 token 或序列；这是一点额外计算换取更稳 off-policy 训练信号。
- **精度影响**：文档说明：RS 会把偏离阈值的 token/序列从 `response_mask` 中排除，用于降低训练-推理不匹配导致的 RL collapse 风险；阈值过严会丢弃过多样本、降低样本效率。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:42` ROLLOUT_RS=${ROLLOUT_RS:-token_k1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
