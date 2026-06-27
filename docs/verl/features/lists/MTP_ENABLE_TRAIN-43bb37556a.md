# MTP_ENABLE_TRAIN

- **参数名**：`MTP_ENABLE_TRAIN`
- **分类**：效率
- **中文解释**：文档说明：MTP（Multi-Token Prediction，多 token 预测）训练开关，示例将它写入 `model.mtp.enable_train`；为 `True` 时启用 MTP 训练损失。
- **常见值**：True
- **来源环境变量**：MTP_ENABLE_TRAIN
- **性能影响**：机制推断：开启后会引入 MTP 辅助预测头相关前向/反向与 loss 计算，增加显存、激活和优化器开销；关闭可减少训练阶段 MTP 额外成本。
- **精度影响**：文档说明：该开关使 MTP loss 参与训练；当 `mtp_loss_scaling_factor` 为非零时会改变优化目标，可能提升 speculative/draft token 质量，也可能因权重设置不当扰动主任务收敛。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:86` MTP_ENABLE_TRAIN=${MTP_ENABLE_TRAIN:-True}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
