# actor_rollout_ref.actor.ppo_epochs

- **参数名**：`actor_rollout_ref.actor.ppo_epochs`
- **分类**：算法
- **中文解释**：文档说明：Actor 对同一批采样轨迹执行 PPO 更新的 epoch 数；Verl PPO README 明确说明它是 actor 在一组 sampled trajectories 上的更新轮数。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：机制推断：增大后同一批 rollout 会执行更多 actor 更新，训练计算时间近似增加，但可能提高样本复用率。
- **精度影响**：机制推断：更多 epoch 可更充分利用样本，但过多会增加 off-policy 偏移、过拟合当前 rollout 或 PPO clip 触发，影响稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`
- `examples/tutorial/skypilot/verl-grpo.yaml`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:89` actor_rollout_ref.actor.ppo_epochs=${ppo_epochs}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:86` actor_rollout_ref.actor.ppo_epochs=${ppo_epochs}
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:110` actor_rollout_ref.actor.ppo_epochs=1
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:110` actor_rollout_ref.actor.ppo_epochs=1
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:102` actor_rollout_ref.actor.ppo_epochs=1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
