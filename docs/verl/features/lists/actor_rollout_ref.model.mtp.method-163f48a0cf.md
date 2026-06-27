# actor_rollout_ref.model.mtp.method

- **参数名**：`actor_rollout_ref.model.mtp.method`
- **分类**：效率
- **中文解释**：文档说明：MTP rollout 中传给 vLLM speculative decoding 的方法名；官方 MTP 文档给出的 vLLM 配置是 `enable_rollout=True`、`method=\"mtp\"` 和 `num_speculative_tokens`。
- **常见值**：mtp
- **来源环境变量**：无
- **性能影响**：文档说明：MTP speculative rollout 可提升接受率，但官方性能说明指出在 H20 上总体吞吐不一定提升，甚至可能下降；实际收益取决于模型、硬件和 draft/verify 配置。
- **精度影响**：机制推断：`method` 只是选择 speculative 路径，不直接改变 MTP loss；只要目标模型验证逻辑正确，输出分布应由目标模型决定，主要风险是后端兼容性或 draft 权重不匹配。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:131` actor_rollout_ref.model.mtp.method=mtp

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
