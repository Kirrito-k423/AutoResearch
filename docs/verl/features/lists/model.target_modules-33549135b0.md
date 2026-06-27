# model.target_modules

- **参数名**：`model.target_modules`
- **分类**：效率
- **中文解释**：指定 LoRA adapter 注入哪些模型模块；官方参数表中对应 `actor_rollout_ref.model.target_modules`，常见值 `all-linear` 表示覆盖所有线性层。
- **常见值**：all-linear
- **来源环境变量**：LORA_TARGETS
- **性能影响**：机制推断：目标模块越多，LoRA 参数、梯度和 adapter 计算越多，checkpoint 也更大；只选择少量模块可降低开销。
- **精度影响**：机制推断：目标模块范围决定可学习更新覆盖面；范围过窄可能欠适配，范围过宽表达力更强但可能增加过拟合或训练波动。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:43` "model.target_modules=${LORA_TARGETS}"
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:53` "model.target_modules=${LORA_TARGETS}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
