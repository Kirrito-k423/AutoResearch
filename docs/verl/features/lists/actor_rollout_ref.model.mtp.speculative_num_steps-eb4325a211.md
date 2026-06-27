# actor_rollout_ref.model.mtp.speculative_num_steps

- **参数名**：`actor_rollout_ref.model.mtp.speculative_num_steps`
- **分类**：效率
- **中文解释**：文档说明：SGLang MTP/EAGLE speculative decoding 的推测步数，控制 draft/verify 循环中连续推测的深度；官方配置表默认值为 3。
- **常见值**：3
- **来源环境变量**：SPEC_NUM_STEPS
- **性能影响**：机制推断：步数越多潜在并行推测越深，但 draft 计算、KV/缓存占用和验证失败回退也更多；过大时可能像官方 H20 观察那样吞吐下降。
- **精度影响**：机制推断：验证正确时主要影响速度，不改变 RL 训练目标；过深推测若后端实现不稳定或权重同步滞后，可能让 rollout 质量/时延波动变大。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:137` actor_rollout_ref.model.mtp.speculative_num_steps=${spec_num_steps}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
