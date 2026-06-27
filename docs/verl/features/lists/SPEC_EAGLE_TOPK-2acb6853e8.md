# SPEC_EAGLE_TOPK

- **参数名**：`SPEC_EAGLE_TOPK`
- **分类**：效率
- **中文解释**：控制 SGLang + EAGLE speculative decoding 的 EAGLE Top-K 候选宽度，映射到 `actor_rollout_ref.model.mtp.speculative_eagle_topk`；示例默认 1。
- **常见值**：1
- **来源环境变量**：SPEC_EAGLE_TOPK
- **性能影响**：机制推断：Top-K 越大，draft 阶段可探索候选越多，可能提高接受率但增加 draft/排序计算；Top-K 较小开销低但潜在加速空间有限。
- **精度影响**：机制推断：在严格校验的 speculative decoding 中通常不改变最终采样分布；如果后端近似或候选选择实现有差异，可能间接改变 rollout 轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:46` spec_eagle_topk=${SPEC_EAGLE_TOPK:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
