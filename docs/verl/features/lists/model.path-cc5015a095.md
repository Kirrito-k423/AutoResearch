# model.path

- **参数名**：`model.path`
- **分类**：配置
- **中文解释**：指定模型权重或模型 ID，是模型规模、结构、显存占用和任务能力的来源。
- **常见值**："${MODEL_PATH}"、$MODEL_ID、$MODEL_PATH、ByteDance-Seed/Seed-OSS-36B-Base、Qwen/Qwen2.5-0.5B-Instruct、Qwen/Qwen2.5-Math-7B、Qwen/Qwen3-30B-A3B-Base、Qwen/Qwen3.5-397B-A17B、deepseek-ai/deepseek-coder-6.7b-instruct、google/gemma-1.1-7b-it、google/gemma-2b-it
- **来源环境变量**：MODEL_PATH
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：14
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
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:32` model.path="${MODEL_PATH}" \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:88` model.path=$MODEL_ID \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:35` "model.path=${MODEL_PATH}"
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:29` model.path=Qwen/Qwen2.5-0.5B-Instruct \
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh:22` model.path=google/gemma-2b-it \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
