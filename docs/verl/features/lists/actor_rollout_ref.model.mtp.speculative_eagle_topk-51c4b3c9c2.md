# actor_rollout_ref.model.mtp.speculative_eagle_topk

- **参数名**：`actor_rollout_ref.model.mtp.speculative_eagle_topk`
- **分类**：效率
- **中文解释**：文档说明：SGLang EAGLE speculative decoding 的 top-k 候选数，用于控制 EAGLE draft 阶段保留多少候选 token；默认配置和本示例常见值为 1。
- **常见值**：1
- **来源环境变量**：SPEC_EAGLE_TOPK
- **性能影响**：机制推断：top-k 越大 draft 搜索空间越宽，可能提高候选覆盖但增加 draft 计算/内存和验证开销；top-k 过小则成本低但接受率可能受限。
- **精度影响**：机制推断：严格验证下主要影响接受率而非目标模型分布；若候选设置导致 draft 质量差，会降低加速收益并增加 rollout 时延波动。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:138` actor_rollout_ref.model.mtp.speculative_eagle_topk=${spec_eagle_topk}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
