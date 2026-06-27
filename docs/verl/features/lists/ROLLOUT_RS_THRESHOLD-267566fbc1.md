# ROLLOUT_RS_THRESHOLD

- **参数名**：`ROLLOUT_RS_THRESHOLD`
- **分类**：效率
- **中文解释**：控制 `algorithm.rollout_correction.rollout_rs_threshold`，即 rejection sampling 的阈值；对 `*k1` 比率模式可写成 `lower_upper`，示例 `0.6_1.6` 表示保留比率落在该区间内的 token/序列。
- **常见值**：0.6_1.6
- **来源环境变量**：ROLLOUT_RS_THRESHOLD
- **性能影响**：机制推断：阈值越严格，被 mask 的 token/序列越多，有效 batch 与可用训练信号越少；阈值越宽则保留样本更多，但 off-policy 偏差更大。
- **精度影响**：文档说明：该阈值直接控制哪些 rollout 样本被视为偏差过大而拒绝，是稳定性与样本效率之间的取舍；过严可能引入选择偏差，过松可能放大训练-推理不匹配。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:43` ROLLOUT_RS_THRESHOLD=${ROLLOUT_RS_THRESHOLD:-0.6_1.6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
