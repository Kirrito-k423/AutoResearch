# engine.activation_checkpointing

- **参数名**：`engine.activation_checkpointing`
- **分类**：效率
- **中文解释**：文档说明：Automodel/SFT engine 是否启用 activation checkpointing；engine 配置说明该开关会在 FSDP2、Megatron-FSDP 或 DDP distributed config 中传入。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：启用后用重算换显存，能降低激活显存并支持更长序列/更大 batch，但反向传播需要额外前向计算，单步时间通常增加。
- **精度影响**：机制推断：checkpointing 目标上保持数学等价，不直接改变 loss；但重算路径、混合精度和确定性设置可能带来极小数值差异，主要收益是避免 OOM。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:46` engine.activation_checkpointing=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
