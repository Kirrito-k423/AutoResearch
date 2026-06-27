# model.mtp.enable

- **参数名**：`model.mtp.enable`
- **分类**：效率
- **中文解释**：启用模型的 MTP（Multi-Token Prediction，多 token 预测）模块；官方参数表写明 `mtp.enable` 控制是否启用 MTP，Qwen3.5 SFT 示例注释也说明该开关会打开 MTP module。
- **常见值**：True
- **来源环境变量**：MTP_ENABLE
- **性能影响**：文档说明：开启 MTP 会引入额外模块和训练/推理相关计算，训练阶段通常增加显存与计算；若配合推测解码使用，可能改善生成阶段吞吐。
- **精度影响**：机制推断：MTP 会加入多 token 预测相关能力/辅助目标，可能改善 draft/speculative token 质量；若损失权重或训练设置不当，也可能扰动主任务收敛。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:92` model.mtp.enable=True \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:24` #   - model.mtp.enable=True               enables MTP module
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:148` model.mtp.enable=${MTP_ENABLE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
