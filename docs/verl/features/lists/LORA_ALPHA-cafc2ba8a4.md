# LORA_ALPHA

- **参数名**：`LORA_ALPHA`
- **分类**：效率
- **中文解释**：文档说明：LoRA 低秩适配器的 alpha 缩放系数；Verl LoRA 文档称其为 LoRA 的 alpha term/Megatron LoRA 低秩投影权重因子，默认示例常见 32。
- **常见值**：16、32、64
- **来源环境变量**：LORA_ALPHA
- **性能影响**：机制推断：alpha 主要是缩放系数，不显著改变参数量或吞吐；与 LoRA merge/refit 配置一起使用时，性能更多由 rank、同步和是否合并决定。
- **精度影响**：机制推断：alpha 改变低秩更新的有效强度；过大可能使适配更新过激，过小可能学习不足，需要与 rank 和学习率共同调节。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:29` LORA_ALPHA=${LORA_ALPHA:-16}
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:36` LORA_ALPHA=${LORA_ALPHA:-16}
- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh:23` lora_alpha=${LORA_ALPHA:-32}
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:23` lora_alpha=${LORA_ALPHA:-64}
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh:23` lora_alpha=${LORA_ALPHA:-32}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
