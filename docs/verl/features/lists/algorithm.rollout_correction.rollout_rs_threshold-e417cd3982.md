# algorithm.rollout_correction.rollout_rs_threshold

- **参数名**：`algorithm.rollout_correction.rollout_rs_threshold`
- **分类**：效率
- **中文解释**：文档说明：Rollout Correction rejection sampling 的阈值配置。对 `*k1` 比率模式可写成 `lower_upper`（如 `0.6_1.6`），对 `*k2/*k3` 模式则提供正的上界；单个阈值会广播到多个 RS 选项。
- **常见值**："null"、0.6_1.6
- **来源环境变量**：ROLLOUT_RS_THRESHOLD
- **性能影响**：机制推断：阈值越严格，被 mask 的 token/序列越多，有效 batch 和可用训练信号减少；阈值越宽，保留样本更多但 off-policy 偏差更大。
- **精度影响**：文档说明：该阈值直接控制哪些 rollout 样本被视为偏差过大而拒绝，是稳定性与样本效率之间的取舍；过严可能引入选择偏差，过松可能放大训练-推理不匹配。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:73` algorithm.rollout_correction.rollout_rs_threshold=${rollout_rs_threshold}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:88` algorithm.rollout_correction.rollout_rs_threshold=${ROLLOUT_RS_THRESHOLD}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
