# engine.override_transformer_config.recompute_num_layers

- **参数名**：`engine.override_transformer_config.recompute_num_layers`
- **分类**：效率
- **中文解释**：用重算换激活显存，适合长序列或大模型，但会增加计算时间。
- **常见值**：1、1"
- **来源环境变量**：无
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:67` +engine.override_transformer_config.recompute_num_layers=1
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:62` engine.override_transformer_config.recompute_num_layers=1 \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:124` +engine.override_transformer_config.recompute_num_layers=1"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
