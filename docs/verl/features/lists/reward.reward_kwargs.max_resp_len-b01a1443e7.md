# reward.reward_kwargs.max_resp_len

- **参数名**：`reward.reward_kwargs.max_resp_len`
- **分类**：算法
- **中文解释**：传给 reward manager/reward function 的最大回复长度，用于奖励侧判断输出长度预算，尤其是 DAPO overlong buffer/超长惩罚逻辑。
- **常见值**：8192
- **来源环境变量**：MAX_RESPONSE_LENGTH
- **性能影响**：机制推断：该值本身不增加 rollout 生成长度，主要影响奖励计算中的长度判断；若配合更长 `data.max_response_length`，整体生成和训练成本会上升。
- **精度影响**：文档说明：DAPO 文档和源码使用 `max_resp_len` 计算超长输出惩罚边界；该值会直接影响长度惩罚、reward 标尺和策略学习偏好。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:118` +reward.reward_kwargs.max_resp_len=${max_response_length}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:162` +reward.reward_kwargs.max_resp_len=${max_response_length}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:164` +reward.reward_kwargs.max_resp_len=${max_response_length}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
