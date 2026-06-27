# DATASET_DIR

- **参数名**：`DATASET_DIR`
- **分类**：配置
- **中文解释**：机制推断：示例脚本中的数据集根目录，用来拼接 `TRAIN_FILES`/`VAL_FILES` 等 parquet 路径；例如 GSM8K/MTP SFT 脚本会从该目录读取 `train.parquet`、`eval.parquet` 或同类数据文件。
- **常见值**：~/dataset、~/dataset/rl/gsm8k
- **来源环境变量**：DATASET_DIR
- **性能影响**：机制推断：目录变量本身不改变模型计算；若指向慢速网络盘或缺失文件，会增加数据加载/启动等待或直接导致任务失败。
- **精度影响**：机制推断：路径本身不直接改变精度，但切换目录通常意味着切换训练/验证数据版本，会改变任务分布、评测口径和最终指标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:29` DATASET_DIR=${DATASET_DIR:-~/dataset/rl/gsm8k}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:46` DATASET_DIR=${DATASET_DIR:-~/dataset}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
