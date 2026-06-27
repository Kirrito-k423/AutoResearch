# EP_SIZE

- **参数名**：`EP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：Megatron MoE 的 expert model parallel size，写入 `engine.expert_model_parallel_size`，用于把不同专家分布到多个并行 rank 上。
- **常见值**：32、8
- **来源环境变量**：EP_SIZE
- **性能影响**：文档说明：EP 可降低单卡专家参数/计算压力，是 MoE 大模型扩展的关键并行维度；增大后通常会增加专家路由和 all-to-all 通信，需要匹配网络拓扑。
- **精度影响**：机制推断：合理 EP 切分不改变模型目标；若与专家数、TP/PP 或硬件规模不匹配，可能导致负载不均、OOM 或训练无法启动。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:30` EP_SIZE=${EP_SIZE:-8}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:61` EP_SIZE=${EP_SIZE:-32}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
