# VAL_TOP_P

- **参数名**：`VAL_TOP_P`
- **分类**：算法
- **中文解释**：控制采样分布，直接影响探索、多样性、精度波动和可复现性。
- **常见值**：0.7
- **来源环境变量**：VAL_TOP_P
- **性能影响**：机制推断：top-p 主要改变验证采样分布，通常不显著改变模型前向计算量；较低 top-p 会减少候选尾部采样，采样器开销可能略降但影响远小于模型推理成本。
- **精度影响**：机制推断：直接改变采样分布，影响探索、多样性和评测波动。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:30` val_top_p=${VAL_TOP_P:-0.7}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:71` val_top_p=${VAL_TOP_P:-0.7}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
