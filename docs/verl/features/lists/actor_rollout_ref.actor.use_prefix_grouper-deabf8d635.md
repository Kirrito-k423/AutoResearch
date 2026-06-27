# actor_rollout_ref.actor.use_prefix_grouper

- **参数名**：`actor_rollout_ref.actor.use_prefix_grouper`
- **分类**：效率
- **中文解释**：文档说明：启用 PrefixGrouper，在 GRPO 这类同一 prompt 生成多条响应的训练中按共享前缀复用注意力计算，减少长 prompt 被重复计算的开销。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：PrefixGrouper README 给出 Qwen3-4B、4xH800、`rollout.n=4` benchmark，长上下文下 `update_actor` 可达约 1.70x、step 约 1.27x 加速；限制是当前仅支持 FSDP，并与 dynamic bsz、remove padding、fused kernels、Ulysses SP 等不兼容。
- **精度影响**：机制推断：目标是等价复用共享 prefix 的 attention，不改变 RL 损失；若分组约束、padding/remove-padding 或 batch balance 设置不兼容，可能造成运行失败或样本分组错误。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/prefix_grouper/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/prefix_grouper/run_qwen3_8b_fsdp.sh:58` actor_rollout_ref.actor.use_prefix_grouper=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
