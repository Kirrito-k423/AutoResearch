# actor_rollout_ref.actor.calculate_sum_pi_squared

- **参数名**：`actor_rollout_ref.actor.calculate_sum_pi_squared`
- **分类**：效率
- **中文解释**：文档说明：启用 Actor 在计算 log probability 时额外输出每个 token 的策略概率平方和 `sum_pi_squared`，供 OTB（Optimal Token Baseline）优势估计器计算 token 级基线使用。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：OTB 文档指出该开关需要暴露 logits，因此当前要关闭 fused log-prob kernels；机制上会增加 logits 相关计算、通信/返回张量和显存占用。
- **精度影响**：文档说明：这是使用 `algorithm.adv_estimator=optimal_token_baseline` 或 `tir_optimal_token_baseline` 的必需配置；正确启用后用于降低优势估计方差，未启用时 OTB 训练会缺少必要张量并被 trainer 检查拦截。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/otb_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/otb_trainer/run_qwen3_8b_fsdp.sh:68` actor_rollout_ref.actor.calculate_sum_pi_squared=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
