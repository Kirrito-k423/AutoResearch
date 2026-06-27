# data.custom_cls.path

- **参数名**：`data.custom_cls.path`
- **分类**：配置
- **中文解释**：Verl 数据模块动态导入自定义数据集类的 Python 文件路径；MiniCPM-o 示例指向 `recipe/minicpmo/rl_dataset.py`。
- **常见值**：recipe/minicpmo/rl_dataset.py
- **来源环境变量**：CUSTOM_CLS_PATH
- **性能影响**：机制推断：路径本身无计算开销；被导入的数据集实现会影响 CPU 预处理、I/O、缓存和 batch 构造效率。
- **精度影响**：机制推断：该路径决定训练数据如何解析和过滤，换实现会改变样本字段、标签或多模态处理；路径错误会使任务启动失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:45` data.custom_cls.path=${CUSTOM_CLS_PATH}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
