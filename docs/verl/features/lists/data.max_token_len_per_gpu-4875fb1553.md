# data.max_token_len_per_gpu

- **参数名**：`data.max_token_len_per_gpu`
- **分类**：效率
- **中文解释**：文档说明：SFT/dynamic batch 数据侧每张 GPU 单次处理的最大 token 数；Verl SFT 配置中与 `data.use_dynamic_bsz` 配套，用 token 上限替代固定 micro batch 调参。
- **常见值**：1024、2048、65536、8192
- **来源环境变量**：MAX_LENGTH
- **性能影响**：文档说明：调高可让动态 batch 每次前后向吃进更多 token、提高吞吐，但过高会 OOM；调低会更保守、micro step 增多。
- **精度影响**：机制推断：若样本内容不变则不直接影响精度；过低可能迫使截断、过滤或更小有效 batch，从而改变训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:87` data.max_token_len_per_gpu=65536 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:28` data.max_token_len_per_gpu=1024
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:25` data.max_token_len_per_gpu=2048 \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:82` data.max_token_len_per_gpu=2048 \
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:86` data.max_token_len_per_gpu=2048 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
