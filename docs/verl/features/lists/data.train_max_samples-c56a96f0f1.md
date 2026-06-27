# data.train_max_samples

- **参数名**：`data.train_max_samples`
- **分类**：效率
- **中文解释**：文档说明：训练集最多使用的样本数；官方 config 文档说明设为 `-1` 表示使用完整训练集。
- **常见值**：-1
- **来源环境变量**：无
- **性能影响**：文档说明：限制样本数会减少数据加载、预处理和训练 epoch 成本，便于 smoke test 或小规模调试；`-1` 使用全量数据，成本随数据规模增加。
- **精度影响**：机制推断：减少训练样本会改变训练分布和覆盖面，可能降低泛化或让小样本调试指标不代表全量训练；`-1` 通常更接近正式训练口径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:28` data.train_max_samples=-1 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
