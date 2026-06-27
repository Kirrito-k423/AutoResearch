# algorithm.rollout_correction.bypass_mode

- **参数名**：`algorithm.rollout_correction.bypass_mode`
- **分类**：效率
- **中文解释**：文档说明：Rollout Correction 的旁路模式开关。`True` 时复用 rollout 阶段的 logprob 作为 old logprob，形成 rollout policy 与当前 policy 的两策略校正；`False` 时重新计算 old logprob，走三策略 decoupled correction。
- **常见值**："true"
- **来源环境变量**：无
- **性能影响**：文档说明：bypass 模式可跳过训练阶段 old_log_prob 重算，减少一次模型前向/通信开销；但需要 rollout 阶段已经正确计算并携带 logprob。
- **精度影响**：文档说明：该模式改变 off-policy correction 的策略口径和 loss 形式；可降低推理-训练不匹配处理成本，但若 rollout logprob 与训练 policy 差距大，稳定性依赖 IS/RS 阈值和 PPO clip 设置。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:77` algorithm.rollout_correction.bypass_mode=${bypass_mode}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:74` algorithm.rollout_correction.bypass_mode=${bypass_mode}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
