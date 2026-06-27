# engine.context_parallel_size

- **参数名**：`engine.context_parallel_size`
- **分类**：效率
- **中文解释**：控制上下文/序列并行，主要用于长序列场景降低激活和注意力显存。
- **常见值**：1
- **来源环境变量**：CP_SIZE
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:62` engine.context_parallel_size=${CP_SIZE} \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:58` engine.context_parallel_size=${CP_SIZE}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:67` engine.context_parallel_size=${CP_SIZE} \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:114` engine.context_parallel_size=${CP_SIZE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
