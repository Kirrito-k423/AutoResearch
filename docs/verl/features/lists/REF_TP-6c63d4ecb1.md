# REF_TP

- **参数名**：`REF_TP`
- **分类**：效率
- **中文解释**：文档说明：reference policy 的 Megatron tensor parallel size，示例写入 `actor_rollout_ref.ref.megatron.tensor_model_parallel_size`，通常默认跟随 actor 的 TP。
- **常见值**：${actor_tp
- **来源环境变量**：REF_TP
- **性能影响**：机制推断：增大 TP 可分摊矩阵计算和权重显存，支撑更大模型；也会增加张量并行通信，过大时通信可能抵消收益。
- **精度影响**：机制推断：正确 TP 切分应保持 reference logprob 等价；并行实现和规约顺序可能带来轻微数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:45` ref_tp=${REF_TP:-${actor_tp}}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
