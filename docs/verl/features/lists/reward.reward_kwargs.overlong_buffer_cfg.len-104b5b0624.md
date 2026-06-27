# reward.reward_kwargs.overlong_buffer_cfg.len

- **参数名**：`reward.reward_kwargs.overlong_buffer_cfg.len`
- **分类**：算法
- **中文解释**：文档说明：DAPO overlong buffer 的缓冲区 token 长度；惩罚从 `max_resp_len - len` 开始，到 `max_resp_len` 处达到最大惩罚。
- **常见值**：4096
- **来源环境变量**：OVERLONG_BUFFER_LEN
- **性能影响**：机制推断：该值只参与奖励端长度阈值计算，直接运行开销近乎不变；更大的缓冲区可能通过训练信号间接鼓励更短输出。
- **精度影响**：文档说明：`len` 越大，惩罚越早介入但斜率更平缓；设置过大可能抑制必要的长链路推理，过小则只在接近硬上限时才产生约束。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:116` +reward.reward_kwargs.overlong_buffer_cfg.len=4096
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:159` +reward.reward_kwargs.overlong_buffer_cfg.len=4096
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:161` +reward.reward_kwargs.overlong_buffer_cfg.len=${overlong_buffer_len}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
