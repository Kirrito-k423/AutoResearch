# engine.tp_size

- **参数名**：`engine.tp_size`
- **分类**：效率
- **中文解释**：设置 AutoModel engine 的张量并行（tensor parallel）大小，把线性层/注意力等大矩阵沿张量维度切到多个 rank；examples 中为 1。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：文档说明：TP 可降低单卡权重和激活显存，并提升大矩阵并行度；但会增加 all-reduce/all-gather 等通信，TP 过大时通信开销明显。
- **精度影响**：机制推断：并行切分不直接改变模型目标；不同通信规约顺序可能带来轻微数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:33` engine.tp_size=1 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:36` engine.tp_size=1 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
