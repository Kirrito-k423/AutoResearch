# model.mtp.mtp_loss_scaling_factor

- **参数名**：`model.mtp.mtp_loss_scaling_factor`
- **分类**：算法
- **中文解释**：MTP（Multi-Token Prediction）辅助 loss 的权重系数；示例默认 `0.1`，用于控制 MTP 预测头训练信号在总 loss 中的占比。
- **常见值**：0.1
- **来源环境变量**：MTP_LOSS_SCALING_FACTOR
- **性能影响**：机制推断：系数本身不改变算子数量；但它通常只在启用 MTP 训练时有意义，而 MTP 训练会增加辅助头前向/反向、激活和优化器状态开销。
- **精度影响**：文档说明：MTP README 和配置注释都把它定义为 MTP loss scaling factor；增大权重会强化 speculative/draft token 辅助目标，过大可能扰动主任务收敛，设为 0 则基本关闭该辅助 loss 贡献。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:151` model.mtp.mtp_loss_scaling_factor=${MTP_LOSS_SCALING_FACTOR} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
