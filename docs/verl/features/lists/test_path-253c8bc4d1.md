# test_path

- **参数名**：`test_path`
- **分类**：配置
- **中文解释**：通用/Geo3K 验证集 parquet 路径；示例直接传给 `data.val_files`，用于评估当前策略在该数据集上的表现。
- **常见值**：$HOME/data/geo3k/test.parquet
- **来源环境变量**：test_path
- **性能影响**：文档说明：`data.val_files` 是验证 parquet，可为单个文件或列表；路径本身不改变训练算子，但验证集大小和存储位置会影响评测加载与端到端耗时。
- **精度影响**：机制推断：通常不直接参与训练梯度；但它决定验证指标的数据口径，并可能影响 checkpoint 选择、实验比较和调参判断。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:86` test_path=${test_path:-$HOME/data/geo3k/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
