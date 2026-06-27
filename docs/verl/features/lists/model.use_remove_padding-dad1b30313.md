# model.use_remove_padding

- **参数名**：`model.use_remove_padding`
- **分类**：效率
- **中文解释**：文档说明：启用 remove padding/sequence packing，使支持的模型把有效 token 打包计算，减少 padding token 带来的无效算力。
- **常见值**：False、True、true
- **来源环境变量**：USE_REMOVE_PADDING
- **性能影响**：文档说明：官方 perf tuning 将其列为性能优化项，支持 llama/mistral/gemma/qwen 等模型；启用后通常减少无效计算并提升吞吐/显存效率。
- **精度影响**：机制推断：正确实现时不改变有效 token 序列；未测试模型或不兼容 packing 可能造成 mask/position 处理错误，需验证。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：13
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:30` #     - model.use_remove_padding=False           (deprecated option, will be removed in the future forces bshd compute format)
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:15` #     - model.use_remove_padding=False           (deprecated option, will be removed in the future forces bshd compute format)
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:33` model.use_remove_padding=true \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:89` model.use_remove_padding=${USE_REMOVE_PADDING} \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:37` model.use_remove_padding=true

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
