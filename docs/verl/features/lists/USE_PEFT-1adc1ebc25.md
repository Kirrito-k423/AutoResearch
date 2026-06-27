# USE_PEFT

- **参数名**：`USE_PEFT`
- **分类**：效率
- **中文解释**：示例说明：SFT 脚本中的 LoRA/PEFT 开关；为 `1` 时追加 `model.lora_rank`、`model.lora_alpha` 和 `model.target_modules`，只训练适配器相关参数。
- **常见值**：0、1
- **来源环境变量**：USE_PEFT
- **性能影响**：机制推断：开启 PEFT 通常显著减少可训练参数、优化器状态和显存需求，但会增加少量 LoRA 前向分支；关闭则更接近全量微调，资源需求更高。
- **精度影响**：机制推断：PEFT 限制可训练容量，低资源场景更稳且成本低，但上限可能低于全量微调；具体效果取决于 rank、目标模块和数据规模。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:27` USE_PEFT=${USE_PEFT:-1}
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:34` USE_PEFT=${USE_PEFT:-0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
