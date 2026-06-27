# LORA_TARGETS

- **参数名**：`LORA_TARGETS`
- **分类**：效率
- **中文解释**：机制推断：LoRA/PEFT 启用时的目标模块选择，脚本把它写入 `model.target_modules`；`all-linear` 表示尽量对线性层挂载 LoRA 适配器。
- **常见值**：all-linear
- **来源环境变量**：LORA_TARGETS
- **性能影响**：机制推断：目标模块越多，可训练 LoRA 参数、显存和额外矩阵乘开销越大；目标模块较少则更省资源但表达能力受限。
- **精度影响**：机制推断：直接影响 PEFT 的可训练容量和适配范围；`all-linear` 通常容量更强，但也更容易增加过拟合或训练不稳定风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:30` LORA_TARGETS=${LORA_TARGETS:-all-linear}
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:37` LORA_TARGETS=${LORA_TARGETS:-all-linear}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
