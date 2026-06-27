# data.pad_mode

- **参数名**：`data.pad_mode`
- **分类**：效率
- **中文解释**：文档说明：控制 SFT 数据 collator 的 padding 方式；`no_padding` 让样本按可变长度批处理，避免把每条样本都补到固定长度，当前 examples 主要用于 Megatron/Automodel/FSDP 的 SFT 长序列路径。
- **常见值**：no_padding
- **来源环境变量**：PAD_MODE
- **性能影响**：机制推断：`no_padding` 可减少 padding token 带来的无效计算和显存占用，但要求后端支持无填充/变长批处理；固定 padding 更简单但长短样本差异大时浪费更明显。
- **精度影响**：机制推断：padding 方式本身通常不改变监督信号；但若与 `data.max_length`、`truncation` 或后端支持不匹配，可能触发截断、报错或 batch 形状差异，从而间接影响可训练样本。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:84` data.pad_mode=${PAD_MODE} \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:29` data.pad_mode=no_padding
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:22` data.pad_mode=no_padding \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:79` data.pad_mode=${PAD_MODE} \
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:82` data.pad_mode=${PAD_MODE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
