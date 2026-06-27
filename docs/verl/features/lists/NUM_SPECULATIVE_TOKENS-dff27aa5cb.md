# NUM_SPECULATIVE_TOKENS

- **参数名**：`NUM_SPECULATIVE_TOKENS`
- **分类**：效率
- **中文解释**：文档说明：vLLM 后端的 MTP speculative decoding 参数，示例注释说明它控制每次 verify step 由 MTP 方法提出的 speculative token 数量。
- **常见值**：3
- **来源环境变量**：NUM_SPECULATIVE_TOKENS
- **性能影响**：机制推断：数值越大，单次 draft 覆盖的 token 越多，接受率高时可减少解码轮次；接受率低时会增加无效 draft 和校验开销。
- **精度影响**：机制推断：带校验的 speculative decoding 通常不应改变采样分布；过大的 draft budget 若与模型/后端实现不匹配，可能通过生成稳定性或失败重试间接影响 rollout 数据。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:41` num_speculative_tokens=${NUM_SPECULATIVE_TOKENS:-3}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
