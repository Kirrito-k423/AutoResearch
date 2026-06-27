# actor_rollout_ref.model.mtp.num_speculative_tokens

- **参数名**：`actor_rollout_ref.model.mtp.num_speculative_tokens`
- **分类**：效率
- **中文解释**：文档说明：vLLM MTP speculative decoding 每轮尝试预测/草拟的 speculative token 数；官方 MTP 文档示例为 1，本 batch 示例通过环境变量设为 3。
- **常见值**：3
- **来源环境变量**：NUM_SPECULATIVE_TOKENS
- **性能影响**：文档说明：MTP rollout 加速依赖接受率；增加 speculative token 可能减少目标模型解码轮数，但 draft 计算和验证失败会抵消收益，官方 H20 示例中吞吐可能下降。
- **精度影响**：机制推断：在严格验证的 speculative decoding 中，该值主要影响速度和接受率，不应改变目标模型分布；过高导致接受率低时会增加延迟和训练采样不稳定感。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:132` actor_rollout_ref.model.mtp.num_speculative_tokens=${num_speculative_tokens}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
