# reward_model.reward_kwargs.overlong_buffer_cfg.enable

- **参数名**：`reward_model.reward_kwargs.overlong_buffer_cfg.enable`
- **分类**：算法
- **中文解释**：文档说明：在 `reward_model` 路径下启用 DAPO 奖励管理器的 overlong buffer 惩罚，对接近最大响应长度的回复施加线性负奖励。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：奖励计算只增加轻量的长度判断和标量加法；训练信号可能促使模型减少冗长输出，从而间接影响 rollout token 开销。
- **精度影响**：文档说明：改变奖励目标以惩罚超长输出，有利于长度控制；若任务答案天然较长，需要配合 `len` 和 `penalty_factor` 避免过惩罚。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:127` +reward_model.reward_kwargs.overlong_buffer_cfg.enable=True \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:106` +reward_model.reward_kwargs.overlong_buffer_cfg.enable=${enable_overlong_buffer}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:108` +reward_model.reward_kwargs.overlong_buffer_cfg.enable=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
