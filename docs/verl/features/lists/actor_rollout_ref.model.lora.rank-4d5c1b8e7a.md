# actor_rollout_ref.model.lora.rank

- **参数名**：`actor_rollout_ref.model.lora.rank`
- **分类**：效率
- **中文解释**：文档说明：Megatron LoRA 的低秩投影维度；设为 0 可关闭 LoRA，常见可用值包括 8/16/32/64，本 batch 示例为 32。
- **常见值**：32
- **来源环境变量**：LORA_RANK
- **性能影响**：文档说明：LoRA 只训练低秩矩阵以降低显存和计算；rank 越大，adapter 参数量、梯度同步、保存和 merge/refit 开销越高。
- **精度影响**：文档说明：Verl LoRA notes 明确提醒过小 rank 会拖慢收敛或降低训练表现；较高 rank 提供更强适配容量，更接近全量微调。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh:62` actor_rollout_ref.model.lora.rank=${lora_rank}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
