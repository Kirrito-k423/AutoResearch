# reward_model.reward_kwargs.overlong_buffer_cfg.len

- **参数名**：`reward_model.reward_kwargs.overlong_buffer_cfg.len`
- **分类**：算法
- **中文解释**：文档说明：`reward_model` 路径下 DAPO overlong buffer 的缓冲 token 数；源码按 `max_resp_len - len` 计算开始扣分的位置。
- **常见值**：$((1024 * 1))、$((1024 * 4))、4096
- **来源环境变量**：无
- **性能影响**：机制推断：直接计算成本基本不变；更大缓冲区会更早给出长度惩罚信号，可能间接减少模型输出长度。
- **精度影响**：文档说明：控制惩罚曲线覆盖的响应尾部区间；过大可能压制合理长推理，过小则主要防止贴近硬上限的极端长输出。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:128` +reward_model.reward_kwargs.overlong_buffer_cfg.len=$((1024 * 4)) \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:107` +reward_model.reward_kwargs.overlong_buffer_cfg.len=${overlong_buffer_len}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:109` +reward_model.reward_kwargs.overlong_buffer_cfg.len=4096

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
