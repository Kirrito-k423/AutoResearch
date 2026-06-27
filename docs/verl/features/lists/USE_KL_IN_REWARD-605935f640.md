# USE_KL_IN_REWARD

- **参数名**：`USE_KL_IN_REWARD`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `algorithm.use_kl_in_reward`，控制是否把相对参考模型的 KL 惩罚加入 reward；官方 best practices 写明 PPO 常用 True，GRPO/DAPO 常用 False。
- **常见值**：False
- **来源环境变量**：USE_KL_IN_REWARD
- **性能影响**：机制推断：启用后需要 KL 相关计算和记录；若引入参考 log-prob 计算路径，会增加少量前向/通信开销。
- **精度影响**：文档说明：启用 reward 侧 KL 会强化对参考模型的约束，可降低策略漂移和 reward hacking，但可能压制探索；禁用则更依赖 loss 侧 KL 或其他约束。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:20` use_kl_in_reward=${USE_KL_IN_REWARD:-False}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
