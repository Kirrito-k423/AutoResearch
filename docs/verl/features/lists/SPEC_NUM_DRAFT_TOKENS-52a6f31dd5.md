# SPEC_NUM_DRAFT_TOKENS

- **参数名**：`SPEC_NUM_DRAFT_TOKENS`
- **分类**：效率
- **中文解释**：控制 SGLang + EAGLE 每轮 speculative decoding 生成的 draft token 数，映射到 `actor_rollout_ref.model.mtp.speculative_num_draft_tokens`；示例默认 4。
- **常见值**：4
- **来源环境变量**：SPEC_NUM_DRAFT_TOKENS
- **性能影响**：文档说明：MTP 文档把 `speculative_num_draft_tokens` 列为 SGLang rollout 加速核心参数；draft token 越多，单次验证潜在推进越多，但接受率不足时会浪费 draft 计算并拖慢吞吐。
- **精度影响**：机制推断：严格 speculative decoding 通过 verifier 接受/拒绝 draft，理论上不改变采样目标；实际训练中需监控接受率、logprob 和后端兼容性，避免 rollout 分布异常。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:47` spec_num_draft_tokens=${SPEC_NUM_DRAFT_TOKENS:-4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
