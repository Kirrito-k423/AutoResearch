# USE_KL_LOSS

- **参数名**：`USE_KL_LOSS`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.actor.use_kl_loss`，控制是否在 actor loss 中加入 KL loss，用 loss 侧正则约束当前策略接近参考策略。
- **常见值**：True
- **来源环境变量**：USE_KL_LOSS
- **性能影响**：机制推断：主要增加 loss 组合和 KL 统计开销；若参考 log-prob 已在流程中计算，额外成本较小，否则会增加相关前向路径。
- **精度影响**：文档说明：PPO/GRPO 文档说明该选项用于 KL divergence control，且使用 actor KL loss 时通常不再在 reward 中加 KL；更强约束可提升稳定性但降低探索。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:22` use_kl_loss=${USE_KL_LOSS:-True}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
