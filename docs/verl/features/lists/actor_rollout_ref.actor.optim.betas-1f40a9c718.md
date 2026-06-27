# actor_rollout_ref.actor.optim.betas

- **参数名**：`actor_rollout_ref.actor.optim.betas`
- **分类**：效率
- **中文解释**：机制推断：Actor 优化器的 Adam/AdamW `betas`，分别控制一阶动量和二阶方差估计的指数滑动平均；示例为 `[0.9,0.98]`。
- **常见值**：[0.9,0.98]
- **来源环境变量**：无
- **性能影响**：机制推断：几乎不改变每步计算量或显存规模，只改变优化器状态更新的衰减系数，性能影响通常很小。
- **精度影响**：机制推断：会影响收敛速度和稳定性；较高 `beta2` 会更平滑梯度方差但响应更慢，需要与学习率、batch size 和 RL 信号噪声一起调节。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:91` actor_rollout_ref.actor.optim.betas=[0.9,0.98]

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
