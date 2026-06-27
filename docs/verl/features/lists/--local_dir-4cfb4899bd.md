# --local_dir

- **参数名**：`--local_dir`
- **分类**：配置
- **中文解释**：文档说明：数据预处理脚本的本地输出目录，用来保存生成的 `train.parquet`、`test.parquet` 和示例 JSON；部分脚本提示该参数已被 `--local_save_dir` 替代但仍兼容。
- **常见值**：~/data/gsm8k、~/data/math
- **来源环境变量**：无
- **性能影响**：机制推断：主要影响数据写入和后续读取位置；本地高速盘通常更快，网络盘或慢盘会拖慢预处理和训练数据加载。
- **精度影响**：机制推断：目录本身不改变算法；只有当目录指向错误数据版本、残留旧 parquet 或缺失文件时，才会通过数据口径影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:24` python3 "$(pwd)/examples/data_preprocess/gsm8k.py" --local_dir ~/data/gsm8k
- `examples/tutorial/skypilot/verl-grpo.yaml:21` python3 "$(pwd)/examples/data_preprocess/math_dataset.py" --local_dir ~/data/math
- `examples/tutorial/skypilot/verl-ppo.yaml:24` python3 "$(pwd)/examples/data_preprocess/gsm8k.py" --local_dir ~/data/gsm8k

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
