# EP

- **参数名**：`EP`
- **分类**：效率
- **中文解释**：文档说明：examples 中的 `EP` 环境变量通常映射到 Megatron `expert_model_parallel_size`，即 MoE 专家并行度；它把不同专家切分/放置到不同设备上。
- **常见值**：1、8
- **来源环境变量**：EP
- **性能影响**：文档说明：EP 需要与 TP/PP/ETP/CP 和硬件拓扑一起平衡；增大 EP 可降低单卡专家权重/计算压力，但会增加 MoE token dispatch/all-to-all 通信和调度复杂度。
- **精度影响**：机制推断：并行度本身应保持数学等价；但通信顺序、非确定性归约或错误的专家切分配置可能带来细小数值差异，配置不当还会造成 OOM/通信失败而无法训练。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:18` EP=${EP:-8}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:57` EP=${EP:-8}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:66` EP=${EP:-8}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:41` EP=${EP:-8}
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:60` EP=${EP:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
