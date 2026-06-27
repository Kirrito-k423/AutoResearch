# USE_REMOVE_PADDING

- **参数名**：`USE_REMOVE_PADDING`
- **分类**：效率
- **中文解释**：文档说明：SFT 示例环境变量，最终写入 `model.use_remove_padding`，控制模型是否移除输入和响应中的 padding token。
- **常见值**：False、True
- **来源环境变量**：USE_REMOVE_PADDING
- **性能影响**：文档说明：Verl config 文档明确说明开启后会移除 padding token，并“很大程度”提升模型运行效率；长短样本差异越大收益通常越明显。
- **精度影响**：机制推断：正确的 remove padding 会保持有效 token/loss mask 不变，通常不直接影响精度；与不兼容特性组合时可能报错或改变样本处理。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:31` USE_REMOVE_PADDING=${USE_REMOVE_PADDING:-True}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:35` USE_REMOVE_PADDING=${USE_REMOVE_PADDING:-True}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:11` USE_REMOVE_PADDING=${USE_REMOVE_PADDING:-False}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
