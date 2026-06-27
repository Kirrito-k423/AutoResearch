# ROLLOUT_TOP_P

- **参数名**：`ROLLOUT_TOP_P`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.top_p`，即 nucleus/Top-P 采样阈值，用累计概率限制候选 token 集合。
- **常见值**：1
- **来源环境变量**：ROLLOUT_TOP_P
- **性能影响**：机制推断：对大模型前向成本影响较小，主要改变采样后处理候选集；可能通过输出多样性和 EOS 分布间接影响生成时长。
- **精度影响**：文档说明：官方最佳实践建议 rollout 保持足够随机性；调低 top_p 会收窄探索，调高更接近全分布采样。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:61` rollout_top_p=${ROLLOUT_TOP_P:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
