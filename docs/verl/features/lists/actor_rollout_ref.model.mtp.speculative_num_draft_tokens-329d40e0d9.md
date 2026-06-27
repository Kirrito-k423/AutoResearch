# actor_rollout_ref.model.mtp.speculative_num_draft_tokens

- **参数名**：`actor_rollout_ref.model.mtp.speculative_num_draft_tokens`
- **分类**：效率
- **中文解释**：文档说明：SGLang MTP/EAGLE speculative decoding 每轮生成的 draft token 数；官方配置表默认和本示例常见值为 4。
- **常见值**：4
- **来源环境变量**：SPEC_NUM_DRAFT_TOKENS
- **性能影响**：机制推断：draft token 越多，单轮可尝试跳过的目标模型解码步数越多，但 draft/verify 计算和失败回退成本也增加；需要结合接受率和硬件吞吐调优。
- **精度影响**：机制推断：严格验证时不直接改变最终 token 分布；draft 数过大若接受率低，会增加延迟和资源抖动，间接影响训练节奏。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:139` actor_rollout_ref.model.mtp.speculative_num_draft_tokens=${spec_num_draft_tokens}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
