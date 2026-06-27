# data.max_length

- **参数名**：`data.max_length`
- **分类**：效率
- **中文解释**：文档说明：SFT 数据侧单条样本的最大 token 长度上限；在右填充模式下会补齐/截断到该长度，在 `no_padding` 下仍用于过长样本检查和截断控制。
- **常见值**：1024、2048
- **来源环境变量**：MAX_LENGTH
- **性能影响**：机制推断：上限越大，单样本 token 数、注意力计算、激活显存和 batch padding 成本越高；过小可降低成本但可能丢弃长样本信息。
- **精度影响**：机制推断：直接决定长样本是否被截断或报错；过小会丢失上下文/答案片段，过大通常保留更多监督信息但会限制 batch size、增加 OOM 风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:83` data.max_length=2048 \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:78` data.max_length=2048 \
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:84` data.max_length=1024 \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:139` data.max_length=${MAX_LENGTH} \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:22` data.max_length=2048 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
