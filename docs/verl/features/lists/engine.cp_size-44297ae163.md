# engine.cp_size

- **参数名**：`engine.cp_size`
- **分类**：效率
- **中文解释**：设置 AutoModel engine 的上下文并行（context parallel）大小，用于把长序列维度切到多个并行 rank 上；examples 中为 1，表示不启用额外上下文切分。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：机制推断：增大 `cp_size` 可降低单卡长序列激活/中间张量压力，可能支持更长上下文，但会增加跨 rank 通信与并行调度开销；`cp_size=1` 最简单、通信最少。
- **精度影响**：机制推断：并行切分本身不改变训练目标；但可能带来分布式规约顺序的细小数值差异，或因能训练更长序列而间接改变任务效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:35` engine.cp_size=1 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:38` engine.cp_size=1 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
