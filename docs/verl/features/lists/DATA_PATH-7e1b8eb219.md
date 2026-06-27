# DATA_PATH

- **参数名**：`DATA_PATH`
- **分类**：配置
- **中文解释**：生成示例读取的输入 parquet 数据路径，脚本将它传给 `data.train_files`，作为 rollout-only generation 的 prompt 来源。
- **常见值**：$HOME/data/gsm8k/test.parquet
- **来源环境变量**：DATA_PATH
- **性能影响**：机制推断：主要影响数据读取与准备阶段；大文件、远程存储或慢盘会拖慢启动/读取，但不改变单步模型计算。
- **精度影响**：机制推断：对纯生成任务而言它决定评测/生成样本集合；路径指向不同数据会改变输出分布和后续评测口径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`

## 证据片段

- `examples/generation/run_deepseek_llm_7b.sh:18` DATA_PATH=${DATA_PATH:-$HOME/data/gsm8k/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
