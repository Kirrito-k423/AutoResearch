# actor_rollout_ref.model.lora_alpha

- **参数名**：`actor_rollout_ref.model.lora_alpha`
- **分类**：效率
- **中文解释**：文档说明：LoRA 低秩适配器的 alpha 缩放系数；Verl LoRA 文档称其为 LoRA alpha term，Megatron LoRA 中对应低秩投影的 weighting factor。
- **常见值**：32、64
- **来源环境变量**：LORA_ALPHA
- **性能影响**：机制推断：alpha 只是缩放系数，通常不改变参数量或吞吐；LoRA 训练性能主要由 rank、目标模块、权重同步和是否 merge/refit 决定。
- **精度影响**：机制推断：alpha 改变 LoRA 更新的有效强度；过大可能使适配更新过激，过小可能学习不足，需要与 rank 和学习率共同调节。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh:56` actor_rollout_ref.model.lora_alpha=${lora_alpha}
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:56` actor_rollout_ref.model.lora_alpha=${lora_alpha}
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh:53` actor_rollout_ref.model.lora_alpha=${lora_alpha}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
