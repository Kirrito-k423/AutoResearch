# TOP_P

- **参数名**：`TOP_P`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.top_p` 或验证 `val_kwargs.top_p`，表示 nucleus/Top-P 采样累计概率阈值。
- **常见值**：1.0
- **来源环境变量**：TOP_P
- **性能影响**：机制推断：主要改变采样候选集，对前向计算成本影响小；可能通过输出长度和 EOS 分布间接影响 rollout/验证耗时。
- **精度影响**：文档说明：调低 top_p 会收窄候选集合、降低多样性和方差；调高更接近全分布采样，有利探索但波动更大。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:28` top_p=${TOP_P:-1.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
