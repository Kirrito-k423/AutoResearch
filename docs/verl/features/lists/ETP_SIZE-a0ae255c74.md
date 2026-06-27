# ETP_SIZE

- **参数名**：`ETP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：Megatron MoE 的 expert tensor parallel size，写入 `engine.expert_tensor_parallel_size`，用于在专家内部再做张量并行切分。
- **常见值**：1
- **来源环境变量**：ETP_SIZE
- **性能影响**：文档说明：ETP 可降低单个专家在单卡上的显存与计算压力，但会引入专家内部张量并行通信；通常需要和 TP/EP、MoE 结构及硬件拓扑一起调优。
- **精度影响**：机制推断：并行切分本身不改变优化目标；通信规约顺序不同可能带来极小数值差异，配置不匹配则可能直接失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:31` ETP_SIZE=${ETP_SIZE:-1}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:62` ETP_SIZE=${ETP_SIZE:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
