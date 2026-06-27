# engine.expert_model_parallel_size

- **参数名**：`engine.expert_model_parallel_size`
- **分类**：效率
- **中文解释**：Megatron/engine 级专家并行（EP）大小，用于 MoE 模型把专家分布到多个设备或并行组上。
- **常见值**：1、32、8
- **来源环境变量**：EP、EP_SIZE
- **性能影响**：文档说明：Verl best practices 建议联合 PP/TP/EP/CP 按显存和网络拓扑平衡；增大 EP 可降低单卡专家参数/计算压力，但会增加路由和跨卡通信成本。
- **精度影响**：机制推断：等价并行切分不改变 MoE 数学结果；错误的并行组或通信配置可能导致运行失败或数值不一致。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:56` engine.expert_model_parallel_size=${EP}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:62` engine.expert_model_parallel_size=${EP_SIZE}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:115` engine.expert_model_parallel_size=${EP_SIZE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
