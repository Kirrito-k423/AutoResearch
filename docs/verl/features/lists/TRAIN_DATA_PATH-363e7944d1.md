# TRAIN_DATA_PATH

- **参数名**：`TRAIN_DATA_PATH`
- **分类**：配置
- **中文解释**：router replay 示例中的训练 parquet 路径，脚本将其传给 `data.train_files` 作为 RL 训练样本来源。
- **常见值**：$HOME/data/gsm8k/train.parquet
- **来源环境变量**：TRAIN_DATA_PATH
- **性能影响**：机制推断：主要影响数据加载与预处理；慢存储或大数据集会增加启动和 dataloader 等待时间。
- **精度影响**：机制推断：它决定训练数据分布和样本质量；换路径等同于换训练集，会直接影响学习目标和最终指标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:18` TRAIN_DATA_PATH=${TRAIN_DATA_PATH:-$HOME/data/gsm8k/train.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
