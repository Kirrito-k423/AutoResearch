# data.micro_batch_size_per_gpu

- **参数名**：`data.micro_batch_size_per_gpu`
- **分类**：效率
- **中文解释**：控制 PPO/反向传播分块大小，是显存占用和 step 时间的核心旋钮。
- **常见值**：2、4、64
- **来源环境变量**：MICRO_BATCH_SIZE、MICRO_BATCH_SIZE_PER_GPU
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:31` data.micro_batch_size_per_gpu=${MICRO_BATCH_SIZE_PER_GPU} \
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh:21` data.micro_batch_size_per_gpu=4 \
- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh:19` data.micro_batch_size_per_gpu=4 \
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:81` data.micro_batch_size_per_gpu=2 \
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh:19` data.micro_batch_size_per_gpu=4 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
