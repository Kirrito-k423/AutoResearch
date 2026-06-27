# SPEC_ALGORITHM

- **参数名**：`SPEC_ALGORITHM`
- **分类**：效率
- **中文解释**：控制 SGLang rollout 的 MTP speculative decoding 算法，映射到 `actor_rollout_ref.model.mtp.speculative_algorithm`；示例默认 `EAGLE`。
- **常见值**：EAGLE
- **来源环境变量**：SPEC_ALGORITHM
- **性能影响**：文档说明：MTP 文档将 SGLang 的 `speculative_algorithm=EAGLE` 列为 rollout 加速配置，但也说明 MTP rollout 收益受模型和硬件影响，H20 示例中吞吐可能下降。
- **精度影响**：机制推断：规范的 speculative decoding 会校验 draft token，目标是保持生成分布不变；若后端实现、权重同步或兼容性异常，则可能影响 rollout 样本分布或直接失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:44` spec_algorithm=${SPEC_ALGORITHM:-EAGLE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
