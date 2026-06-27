# CRITIC_LR

- **参数名**：`CRITIC_LR`
- **分类**：算法
- **中文解释**：设置 PPO critic 优化器学习率，对应脚本中的 `critic.optim.lr=${CRITIC_LR}`；官方参数表将 `critic.optim.lr` 说明为 Critic 学习率，常见默认 1e-5。
- **常见值**：1e-5
- **来源环境变量**：CRITIC_LR
- **性能影响**：机制推断：学习率不直接改变单步 FLOPs；合适的 critic 学习率可能减少达到稳定 value estimate 所需的训练步数，过高导致震荡或重跑成本。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:23` CRITIC_LR=${CRITIC_LR:-1e-5}
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:21` critic_lr=${CRITIC_LR:-1e-5}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
