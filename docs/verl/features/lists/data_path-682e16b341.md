# data_path

- **参数名**：`data_path`
- **分类**：配置
- **中文解释**：机制推断：VeOmni/GRPO 示例中的数据根目录变量，脚本用它拼出 `train.parquet` 和 `test.parquet` 路径，常用于 Geo3K 等数据集。
- **常见值**：$HOME/data/geo3k、$HOME/geo3k
- **来源环境变量**：data_path
- **性能影响**：机制推断：主要影响训练/验证 parquet 的读取位置；本地高速存储更利于数据加载，网络盘或错误挂载会拖慢端到端训练。
- **精度影响**：机制推断：路径本身不改变算法；但它决定实际读取的数据集根目录，指向错误数据版本会直接改变训练和评测口径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:16` data_path=${data_path:-$HOME/data/geo3k}
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:10` data_path=${data_path:-$HOME/geo3k}
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:16` data_path=${data_path:-$HOME/data/geo3k}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
