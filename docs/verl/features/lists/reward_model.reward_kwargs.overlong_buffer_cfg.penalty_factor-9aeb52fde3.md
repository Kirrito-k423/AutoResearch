# reward_model.reward_kwargs.overlong_buffer_cfg.penalty_factor

- **参数名**：`reward_model.reward_kwargs.overlong_buffer_cfg.penalty_factor`
- **分类**：算法
- **中文解释**：文档说明：`reward_model` 路径下 DAPO overlong buffer 的最大扣分系数；超过缓冲起点越多，负奖励按比例增加，最多接近 `-penalty_factor`。
- **常见值**：1.0
- **来源环境变量**：无
- **性能影响**：机制推断：只改变奖励标量幅度，直接计算成本基本不变；较强惩罚可能间接缩短模型后续生成。
- **精度影响**：文档说明：直接调节超长输出的负奖励强度；过低可能约束不足，过高可能牺牲需要长答案的样本收益。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:129` +reward_model.reward_kwargs.overlong_buffer_cfg.penalty_factor=1.0 \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:108` +reward_model.reward_kwargs.overlong_buffer_cfg.penalty_factor=${overlong_penalty_factor}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:110` +reward_model.reward_kwargs.overlong_buffer_cfg.penalty_factor=1.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
