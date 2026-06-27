# PP_SIZE

- **参数名**：`PP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：`PP_SIZE` 是 examples 中的 pipeline model parallel size，写入 Megatron/SFT engine 的 `pipeline_model_parallel_size`，用于把模型层切到多个流水阶段。
- **常见值**：1、2、4
- **来源环境变量**：PP_SIZE
- **性能影响**：文档说明：Verl 性能建议要求 PP/TP/EP/ETP/CP 按显存和网络约束平衡；增大 PP 可降低单卡层数和激活显存，但会引入 pipeline bubble、跨阶段通信和调度复杂度。
- **精度影响**：机制推断：不直接改变训练目标；若为了适配 PP 同时改变 micro batch、重计算或 batch 组织，才可能间接影响收敛稳定性。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:25` PP_SIZE=${PP_SIZE:-2}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:27` PP_SIZE=${PP_SIZE:-1}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:7` PP_SIZE=${PP_SIZE:-1}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:58` PP_SIZE=${PP_SIZE:-4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
