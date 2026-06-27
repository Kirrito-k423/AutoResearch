# CUSTOM_CLS_PATH

- **参数名**：`CUSTOM_CLS_PATH`
- **分类**：配置
- **中文解释**：自定义数据集实现文件路径环境变量，示例默认 `recipe/minicpmo/rl_dataset.py`，随后写入 `data.custom_cls.path` 供 Verl 动态导入。
- **常见值**：recipe/minicpmo/rl_dataset.py
- **来源环境变量**：CUSTOM_CLS_PATH
- **性能影响**：机制推断：路径本身无算力影响；导入的自定义数据集实现可能改变 CPU 预处理、缓存、图像读取和批构造耗时。
- **精度影响**：机制推断：自定义数据集代码决定样本字段和标签处理，路径指向不同实现会改变数据语义；路径错误会导致训练无法启动。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:7` CUSTOM_CLS_PATH=${CUSTOM_CLS_PATH:-recipe/minicpmo/rl_dataset.py}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
