# MTP_ENABLE

- **参数名**：`MTP_ENABLE`
- **分类**：效率
- **中文解释**：文档说明：MTP 模块总开关，示例将 `MTP_ENABLE` 写入 `model.mtp.enable`；开启后加载/保存 MTP 参数，但是否训练或用于 rollout 还要看 `enable_train`、`enable_rollout` 等配置。
- **常见值**：True
- **来源环境变量**：MTP_ENABLE
- **性能影响**：文档说明：仅加载 MTP 参数会增加显存占用；若进一步启用 MTP rollout，可用于 speculative/加速 rollout，但实际吞吐收益受模型大小和硬件影响。
- **精度影响**：文档说明：指南列出的无显著影响场景包括“仅携带/加载 MTP 参数但不训练 MTP”；只有 MTP loss 作用到全模型且缩放因子非零时才明显影响训练结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:85` MTP_ENABLE=${MTP_ENABLE:-True}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
