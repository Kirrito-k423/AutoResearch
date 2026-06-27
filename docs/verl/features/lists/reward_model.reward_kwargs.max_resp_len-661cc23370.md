# reward_model.reward_kwargs.max_resp_len

- **参数名**：`reward_model.reward_kwargs.max_resp_len`
- **分类**：算法
- **中文解释**：文档说明：传给 DAPO 奖励管理器的最大响应长度，用来计算 overlong buffer 的惩罚起点；启用 overlong buffer 时源码要求该值存在且不小于缓冲区长度。
- **常见值**：$((1024 * 2))、8192
- **来源环境变量**：MAX_RESPONSE_LENGTH
- **性能影响**：机制推断：作为奖励端长度参考本身几乎不增加开销；若与实际 `data.max_response_length` 保持一致，可避免奖励端额外误判。
- **精度影响**：文档说明：决定 overlong 惩罚的硬上限和阈值基准；设置过低会过早惩罚正常回复，设置过高会削弱长度约束。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:131` +reward_model.reward_kwargs.max_resp_len=${max_response_length} \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:110` +reward_model.reward_kwargs.max_resp_len=${max_response_length}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:112` +reward_model.reward_kwargs.max_resp_len=${max_response_length}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
