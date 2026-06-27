# data.ignore_input_ids_mismatch

- **参数名**：`data.ignore_input_ids_mismatch`
- **分类**：效率
- **中文解释**：文档说明：SFT 配置中该开关用于处理 MultiTurnSFTDataset 分 turn 套 chat template 后拼接的 `input_ids` 与整段 messages 一次性套 template 的结果不一致；设为 true 时忽略 mismatch 并使用拼接后的 `input_ids`。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：几乎不影响吞吐；主要影响是从遇到 mismatch 直接报错变成记录 warning 后继续构造样本。
- **精度影响**：机制推断：可能改变实际训练 token 序列/label 对齐口径；只有在确认 mismatch 是 chat template 的预期差异时才适合开启，否则可能掩盖数据预处理错误。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:27` data.ignore_input_ids_mismatch=True \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:84` data.ignore_input_ids_mismatch=True \
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:53` data.ignore_input_ids_mismatch=True \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:27` data.ignore_input_ids_mismatch=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
