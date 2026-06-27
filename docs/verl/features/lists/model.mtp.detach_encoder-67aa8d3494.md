# model.mtp.detach_encoder

- **参数名**：`model.mtp.detach_encoder`
- **分类**：效率
- **中文解释**：文档说明：MTP 训练开关之一；启用后在多 token 预测辅助损失中 detach/freeze encoder 侧梯度，使 MTP loss 主要更新 MTP 模块参数。
- **常见值**：True
- **来源环境变量**：MTP_DETACH_ENCODER
- **性能影响**：机制推断：detach encoder 可减少 MTP 辅助损失向主干回传的梯度路径和优化器更新范围，通常有利于降低训练开销与显存压力。
- **精度影响**：文档说明：MTP 指南推荐 `detach_encoder=True`；实验说明携带 MTP 参数并训练 MTP 时，detach encoder 对 main loss 影响有限，但会影响 MTP loss 的收敛值。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:26` #   - model.mtp.detach_encoder=True       detaches encoder gradients for MTP
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:150` model.mtp.detach_encoder=${MTP_DETACH_ENCODER} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
