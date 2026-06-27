# algorithm.rollout_correction.rollout_rs

- **参数名**：`algorithm.rollout_correction.rollout_rs`
- **分类**：效率
- **中文解释**：文档说明：Rollout Correction 的 rejection sampling 模式，`null` 表示关闭；如 `token_k1` 表示按 token 级 `-log r` 比率边界过滤 rollout 与训练策略偏差过大的 token/样本。支持多个模式用逗号组合。
- **常见值**："null"、token_k1
- **来源环境变量**：ROLLOUT_RS
- **性能影响**：文档说明：启用后需要计算校正权重和 rejection mask，并可能减少参与 loss 的有效 token/序列；额外计算换取更稳的 off-policy 训练信号。
- **精度影响**：文档说明：用于过滤 rollout policy 与当前/old policy 差异过大的样本，降低训练-推理不匹配导致的 RL collapse 风险；阈值过严会丢弃过多样本、增加偏差或降低样本效率。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:72` algorithm.rollout_correction.rollout_rs=${rollout_rs}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:87` algorithm.rollout_correction.rollout_rs=${ROLLOUT_RS}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
