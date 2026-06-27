# engine.pp_size

- **参数名**：`engine.pp_size`
- **分类**：效率
- **中文解释**：设置 AutoModel engine 的流水线并行（pipeline parallel）大小，把模型层切分到多个 pipeline stage；examples 中为 1，表示不做流水线切分。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：文档说明：PP 可降低单卡层参数和激活压力、支持更大模型，但会引入 pipeline bubble、跨 stage 通信和 microbatch 调度开销。
- **精度影响**：机制推断：流水线切分不改变训练目标；但 microbatch 调度、规约顺序和可训练模型规模变化可能间接影响收敛表现。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:34` engine.pp_size=1 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:37` engine.pp_size=1 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
