# gsm8k_train_path

- **参数名**：`gsm8k_train_path`
- **分类**：配置
- **中文解释**：GSM8K 训练集 parquet 路径；示例把它与 `math_train_path` 组装成 `train_files`，再传给 `data.train_files` 作为 RL 训练数据来源。
- **常见值**：$HOME/data/gsm8k/train.parquet
- **来源环境变量**：gsm8k_train_path
- **性能影响**：文档说明：`data.train_files` 可为单个或列表 parquet，程序会读入内存且支持本地/HDFS 路径；数据大小和远端 I/O 会影响启动、内存占用和数据加载耗时。
- **精度影响**：文档说明：训练数据源决定任务分布，并且需要与 `data_source` 对应的奖励函数匹配；路径指错或数据口径变化会直接改变训练信号和最终效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:20` gsm8k_train_path=${gsm8k_train_path:-$HOME/data/gsm8k/train.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
