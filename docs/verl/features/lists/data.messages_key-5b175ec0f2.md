# data.messages_key

- **参数名**：`data.messages_key`
- **分类**：效率
- **中文解释**：文档说明：SFT 多轮数据集中消息列表的字段名，默认通常为 `messages`；示例也会设成 `prompt`，数据集代码会按该列读取 conversation messages。
- **常见值**：messages、prompt
- **来源环境变量**：无
- **性能影响**：机制推断：主要影响数据读取和预处理字段选择，通常不改变训练吞吐；字段缺失会在数据加载阶段失败，字段内容更长则会通过 token 数间接增加耗时和显存。
- **精度影响**：机制推断：字段选错会把错误或空消息作为监督数据，直接破坏训练信号；字段正确时只是数据 schema 适配，不改变算法本身。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：12
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:30` data.messages_key=messages \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:25` data.messages_key=messages
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:26` data.messages_key=messages \
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh:20` data.messages_key=messages \
- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh:18` data.messages_key=messages \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
