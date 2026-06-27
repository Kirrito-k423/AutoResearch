# ROLLOUT_IS_THRESHOLD

- **参数名**：`ROLLOUT_IS_THRESHOLD`
- **分类**：效率
- **中文解释**：控制 `algorithm.rollout_correction.rollout_is_threshold`，即 Rollout Correction 中 IS 权重的截断阈值；单个数值表示 TIS 上界，`lower_upper` 字符串可表达 IcePop 式上下界过滤。
- **常见值**：2.0
- **来源环境变量**：ROLLOUT_IS_THRESHOLD
- **性能影响**：机制推断：实现上主要是对 IS 权重做 clamp 或区间 mask，额外计算很小；阈值过严会降低有效样本权重，可能间接降低样本利用率。
- **精度影响**：文档说明：该阈值用于截断极端 IS 权重以降低方差、防止 off-policy 偏差导致训练不稳定；阈值越低越保守但偏差更大，阈值越高越保留原始权重但可能放大不稳定。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:40` ROLLOUT_IS_THRESHOLD=${ROLLOUT_IS_THRESHOLD:-2.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
