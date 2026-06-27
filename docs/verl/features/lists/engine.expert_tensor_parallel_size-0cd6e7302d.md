# engine.expert_tensor_parallel_size

- **参数名**：`engine.expert_tensor_parallel_size`
- **分类**：效率
- **中文解释**：设置专家层内部的 tensor parallel 大小，即对 MoE expert 的矩阵参数/计算继续做张量并行切分；Megatron 配置中 `null` 表示跟随普通 TP，examples 显式设为 1。
- **常见值**：1
- **来源环境变量**：ETP_SIZE
- **性能影响**：文档说明：专家 TP 可降低单卡专家层显存和单 rank 计算量，但会增加专家内部张量并行通信；过大时通信成本可能抵消收益。
- **精度影响**：机制推断：只改变专家层并行切分方式，不直接改变模型目标；不同规约顺序可能带来微小数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:63` engine.expert_tensor_parallel_size=${ETP_SIZE}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:116` engine.expert_tensor_parallel_size=${ETP_SIZE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
