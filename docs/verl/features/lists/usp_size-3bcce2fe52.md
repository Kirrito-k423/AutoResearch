# usp_size

- **参数名**：`usp_size`
- **分类**：效率
- **中文解释**：示例脚本中的 Ulysses/sequence parallel size，常被传给 VeOmni actor 的 `ulysses_parallel_size`，用于长上下文训练时沿序列维度并行。
- **常见值**：1、2
- **来源环境变量**：usp_size
- **性能影响**：机制推断：增大 `usp_size` 可降低单卡长序列激活/注意力显存压力，支持更长上下文或更大 batch；代价是序列并行通信和调度开销。
- **精度影响**：机制推断：序列并行不改变训练目标；除浮点归约顺序或通信异常外，通常不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:20` usp_size=${usp_size:-2}
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:18` usp_size=${usp_size:-1}
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:18` usp_size=${usp_size:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
