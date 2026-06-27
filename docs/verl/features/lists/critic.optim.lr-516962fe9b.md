# critic.optim.lr

- **参数名**：`critic.optim.lr`
- **分类**：算法
- **中文解释**：Critic 优化器学习率，控制 value/critic 网络每次更新的步长。
- **常见值**：1e-5
- **来源环境变量**：CRITIC_LR
- **性能影响**：机制推断：不直接影响单步吞吐；过高可能导致 critic 发散、NaN 或重跑，过低可能需要更多训练步数才能学到稳定 value。
- **精度影响**：机制推断：critic 学习率影响 value 拟合质量和 advantage 估计，从而影响 PPO/RL 更新稳定性与最终策略效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:109` critic.optim.lr=${CRITIC_LR}
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:96` critic.optim.lr=${critic_lr}
- `examples/tutorial/skypilot/verl-ppo.yaml:85` critic.optim.lr=1e-5 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
