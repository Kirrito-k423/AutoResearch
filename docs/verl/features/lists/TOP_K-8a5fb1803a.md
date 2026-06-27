# TOP_K

- **参数名**：`TOP_K`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.top_k`，控制 Top-K 采样候选 token 数；官方参数表说明 vLLM rollout 中 `-1` 表示不启用 Top-K 限制。
- **常见值**：-1
- **来源环境变量**：TOP_K
- **性能影响**：机制推断：主要影响采样后处理候选集，对模型前向成本影响小；较小 K 可能略降采样开销，但端到端收益通常不如 batch/并行参数明显。
- **精度影响**：文档说明：官方建议 rollout 可用 `top_k=-1` 保持足够随机性；较小 K 会降低多样性并可能减少探索。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:29` top_k=${TOP_K:--1} # 0 for HF rollout, -1 for vLLM rollout

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
