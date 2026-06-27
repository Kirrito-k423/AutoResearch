# INFER_TP

- **参数名**：`INFER_TP`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧 tensor parallel size 的环境变量，示例默认继承 `ROLLOUT_TP`，最终写入 `actor_rollout_ref.rollout.tensor_model_parallel_size`。
- **常见值**：${rollout_tp
- **来源环境变量**：INFER_TP
- **性能影响**：文档说明：rollout TP 用于推理引擎张量并行；增大可扩展 KV cache/权重容量，但通信成本会上升，特别是 TP 大于 8 时需要关注通信开销。
- **精度影响**：机制推断：正确 TP 切分通常保持推理输出等价；后端支持、并行归约和权重同步差异可能造成轻微数值差异或兼容性问题。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:53` infer_tp=${INFER_TP:-${rollout_tp}}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
