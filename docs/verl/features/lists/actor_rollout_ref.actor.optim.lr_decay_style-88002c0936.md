# actor_rollout_ref.actor.optim.lr_decay_style

- **参数名**：`actor_rollout_ref.actor.optim.lr_decay_style`
- **分类**：算法
- **中文解释**：文档说明：Actor optimizer 的学习率衰减策略；Verl 配置文档列出 `constant`、`linear`、`cosine`、`inverse_square_root` 等，示例中 `constant` 表示 warmup 后保持学习率不继续衰减。
- **常见值**：constant
- **来源环境变量**：无
- **性能影响**：机制推断：不直接改变单步计算量；但会影响收敛速度、稳定训练窗口和需要的调参/训练步数。
- **精度影响**：机制推断：不同衰减曲线会改变后期更新强度；constant 保持更新力度，cosine/linear 更偏向后期收敛稳定，选型会影响最终精度和震荡风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:88` actor_rollout_ref.actor.optim.lr_decay_style=constant

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
