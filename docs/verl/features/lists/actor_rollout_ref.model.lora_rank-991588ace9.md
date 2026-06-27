# actor_rollout_ref.model.lora_rank

- **参数名**：`actor_rollout_ref.model.lora_rank`
- **分类**：效率
- **中文解释**：文档说明：LoRA 低秩投影空间维度；Verl LoRA 文档要求该值设为大于 0 的合理整数来启用 LoRA，常见示例为 32/64。
- **常见值**：32、64
- **来源环境变量**：LORA_RANK
- **性能影响**：文档说明：LoRA 只训练低秩矩阵以降低显存和计算，使大模型能在较少硬件上训练；rank 越大，适配器参数、同步和少量计算开销越高。
- **精度影响**：文档说明：Verl LoRA notes 明确提醒过小 rank 会拖慢收敛或降低训练表现；较高 rank 提供更强适配容量，更接近全量微调。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh:55` actor_rollout_ref.model.lora_rank=${lora_rank}
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:55` actor_rollout_ref.model.lora_rank=${lora_rank}
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh:52` actor_rollout_ref.model.lora_rank=${lora_rank}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
