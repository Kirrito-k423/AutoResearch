# model.lora_rank

- **参数名**：`model.lora_rank`
- **分类**：效率
- **中文解释**：设置 SFT/LoRA adapter 的低秩维度；官方参数表说明 rank 为 0 表示不使用 LoRA，SFT trainer 会用该值构造 adapter 配置。
- **常见值**：32
- **来源环境变量**：LORA_RANK
- **性能影响**：机制推断：rank 越高，LoRA 参数量、梯度、优化器状态和矩阵乘加开销越大；rank 为 0 则关闭 LoRA，资源开销最低。
- **精度影响**：机制推断：rank 控制 adapter 表达能力；较高 rank 可能提升适配能力，但也增加过拟合和训练不稳定风险，较低 rank 更省但可能欠拟合。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:41` "model.lora_rank=${LORA_RANK}"
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:51` "model.lora_rank=${LORA_RANK}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
