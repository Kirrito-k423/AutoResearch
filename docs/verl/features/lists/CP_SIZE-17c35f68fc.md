# CP_SIZE

- **参数名**：`CP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：SFT examples 中的 `CP_SIZE` 环境变量映射到 `engine.context_parallel_size`，控制 Megatron/SFT engine 的上下文并行规模。
- **常见值**：1
- **来源环境变量**：CP_SIZE
- **性能影响**：文档说明：上下文并行可降低长序列单卡显存压力；机制推断：`CP_SIZE` 增大后通信和调度开销上升，需要与 TP/PP/EP 及 batch/token 长度配平。
- **精度影响**：机制推断：正确配置下不改变监督目标；但并行归约顺序和后端实现可能带来微小数值差异，错误配置会导致启动/通信失败。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:27` CP_SIZE=${CP_SIZE:-1}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:29` CP_SIZE=${CP_SIZE:-1}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:9` CP_SIZE=${CP_SIZE:-1}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:60` CP_SIZE=${CP_SIZE:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
