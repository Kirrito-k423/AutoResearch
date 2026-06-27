# engine.ulysses_sequence_parallel_size

- **参数名**：`engine.ulysses_sequence_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：SFT/FSDP 路径的 Ulysses 序列并行大小；设为大于 1 时沿序列维度切分长上下文训练，使不同模型组件可以使用不同的 sequence parallel size。
- **常见值**：1、2
- **来源环境变量**：SP_SIZE
- **性能影响**：文档说明：用于长序列训练降低单卡激活/注意力显存；机制推断：会增加序列并行通信和调度开销，通常需要配合降低 micro batch 或 max token len 避免 OOM。
- **精度影响**：机制推断：序列并行正确实现时保持数学等价；跨设备通信/归约顺序可能带来细小数值差异，主要精度收益来自能训练更长上下文或更合适的 batch。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:35` engine.ulysses_sequence_parallel_size=${SP_SIZE} \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:43` engine.ulysses_sequence_parallel_size=${SP_SIZE} \
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:56` engine.ulysses_sequence_parallel_size=${SP_SIZE} \
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh:21` engine.ulysses_sequence_parallel_size=2 \
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:65` engine.ulysses_sequence_parallel_size=${SP_SIZE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
