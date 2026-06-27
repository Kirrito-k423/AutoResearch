# algorithm.rollout_correction.loss_type

- **参数名**：`algorithm.rollout_correction.loss_type`
- **分类**：算法
- **中文解释**：选择 rollout correction 启用时使用的校正损失类型；官方参数表默认 `ppo_clip`，examples 中还出现 `reinforce`，用于决定校正权重如何进入策略损失。
- **常见值**："ppo_clip"、"reinforce"
- **来源环境变量**：无
- **性能影响**：机制推断：不同 loss_type 的额外计算通常小于 rollout/model 前向成本；若启用 rollout correction，会增加权重、mask 或校正项处理开销。
- **精度影响**：文档说明：该参数直接改变 off-policy/rollout correction 下的策略优化目标；`ppo_clip` 更接近 PPO 裁剪约束，`reinforce` 更接近未裁剪策略梯度，稳定性和偏差/方差会不同。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:78` algorithm.rollout_correction.loss_type=${loss_type}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:75` algorithm.rollout_correction.loss_type=${loss_type}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
