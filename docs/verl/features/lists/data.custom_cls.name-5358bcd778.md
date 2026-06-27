# data.custom_cls.name

- **参数名**：`data.custom_cls.name`
- **分类**：配置
- **中文解释**：Verl 数据模块要从 `data.custom_cls.path` 动态加载的数据集类名；MiniCPM-o 示例使用 `RLHFDataset` 处理 Geo3K 多模态样本。
- **常见值**：RLHFDataset
- **来源环境变量**：CUSTOM_CLS_NAME
- **性能影响**：机制推断：类名本身无性能成本；实际类实现会决定样本解析、图像处理、缓存和 dataloader CPU 开销。
- **精度影响**：机制推断：自定义类会定义 prompt/label/多模态字段如何进入训练，选择不同类会改变数据语义和最终效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:46` data.custom_cls.name=${CUSTOM_CLS_NAME}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
