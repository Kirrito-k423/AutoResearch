# algorithm.rollout_correction.rollout_is_threshold

- **参数名**：`algorithm.rollout_correction.rollout_is_threshold`
- **分类**：效率
- **中文解释**：Rollout Correction 中 IS 权重的截断阈值；单个数值表示 TIS 上界，`lower_upper` 字符串可表示 IcePop 的上下界过滤。
- **常见值**：2.0
- **来源环境变量**：ROLLOUT_IS_THRESHOLD
- **性能影响**：机制推断：主要是一次 clamp 或区间 mask，计算开销很小；阈值过严可能降低有效样本权重，间接影响训练效率。
- **精度影响**：文档说明：源码说明截断极端 IS 权重用于防止训练不稳定；阈值越低偏差越大但方差更低，阈值越高更保留原始权重但可能放大不稳定。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:73` algorithm.rollout_correction.rollout_is_threshold=${rollout_is_threshold}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:70` algorithm.rollout_correction.rollout_is_threshold=${rollout_is_threshold}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:85` algorithm.rollout_correction.rollout_is_threshold=${ROLLOUT_IS_THRESHOLD}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
