# algorithm.kl_penalty

- **参数名**：`algorithm.kl_penalty`
- **分类**：算法
- **中文解释**：选择 actor 与 reference policy 之间 KL divergence 的估计方式；Verl 文档列出 `kl`、`abs`、`mse`、`low_var_kl`、`full` 等选项。
- **常见值**：kl
- **来源环境变量**：无
- **性能影响**：机制推断：通常只是 logprob 张量上的不同 KL 公式，额外计算开销较小；若选择更完整的分布级估计，可能增加内存/计算压力。
- **精度影响**：文档说明：该参数决定 KL 惩罚的估计方式，直接影响策略偏离 reference 的约束强度、reward hacking 风险、探索和训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh`
- `examples/remax_trainer/run_qwen3_8b_fsdp.sh`
- `examples/rloo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/rloo_trainer/run_qwen3_8b_fsdp.sh:44` algorithm.kl_penalty=kl
- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh:44` algorithm.kl_penalty=kl
- `examples/remax_trainer/run_qwen3_8b_fsdp.sh:44` algorithm.kl_penalty=kl

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
