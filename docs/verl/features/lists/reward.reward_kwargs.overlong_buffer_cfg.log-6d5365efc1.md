# reward.reward_kwargs.overlong_buffer_cfg.log

- **参数名**：`reward.reward_kwargs.overlong_buffer_cfg.log`
- **分类**：算法
- **中文解释**：控制 DAPO/overlong buffer 奖励惩罚是否记录额外日志信息；源码中惩罚由 `enable`、`len`、`penalty_factor` 决定，`log=True` 时额外写入 `overlong_reward` 和 `overlong` 信息。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：开启日志会增加少量 reward extra info 记录与内存/日志开销；关闭可减少诊断信息但不影响主要计算。
- **精度影响**：机制推断：`log` 只控制是否记录 overlong 惩罚相关信息，不改变 overlong reward 计算本身；精度影响通常为无。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:161` +reward.reward_kwargs.overlong_buffer_cfg.log=False
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:163` +reward.reward_kwargs.overlong_buffer_cfg.log=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
