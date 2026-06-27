# model.mtp.enable_train

- **参数名**：`model.mtp.enable_train`
- **分类**：效率
- **中文解释**：文档说明：MTP（Multi-Token Prediction）训练开关；在 `model.mtp.enable=True` 基础上开启 MTP 辅助训练 loss，使模型训练时学习多 token 预测能力。
- **常见值**：True
- **来源环境变量**：MTP_ENABLE_TRAIN
- **性能影响**：机制推断：开启 MTP 训练会增加额外 MTP head/loss 的前向、反向和激活保存开销；若后续用于推测解码，可能为 rollout 加速能力提供训练基础。
- **精度影响**：文档说明：MTP 指南说明 full-parameter MTP training 会让 MTP loss 作用到所有模型参数；实验记录显示 MTP 层存在对 main loss 影响有限，但 detach 与 loss scaling 会改变 MTP loss 行为。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:25` #   - model.mtp.enable_train=True         enables MTP training loss
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:149` model.mtp.enable_train=${MTP_ENABLE_TRAIN} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
