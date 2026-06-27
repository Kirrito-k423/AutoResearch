# VPP_SIZE

- **参数名**：`VPP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：`VPP_SIZE` 是 virtual pipeline model parallel size，写入 `virtual_pipeline_model_parallel_size`；用于 Megatron 流水并行的虚拟 stage/交错调度，`null` 表示不启用该切分。
- **常见值**：null
- **来源环境变量**：VPP_SIZE
- **性能影响**：机制推断：合适的 VPP 可降低 pipeline bubble、改善 stage 利用率；不合适的值会增加调度复杂度、激活驻留和通信同步成本。
- **精度影响**：机制推断：不直接改变训练目标；主要风险来自与 PP、micro batch、layer 切分不匹配导致运行失败或有效 batch 调整。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:26` VPP_SIZE=${VPP_SIZE:-null}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:28` VPP_SIZE=${VPP_SIZE:-null}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:8` VPP_SIZE=${VPP_SIZE:-null}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:59` VPP_SIZE=${VPP_SIZE:-null}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
