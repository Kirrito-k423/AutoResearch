# CUSTOM_CLS_NAME

- **参数名**：`CUSTOM_CLS_NAME`
- **分类**：配置
- **中文解释**：自定义数据集类名环境变量，示例默认 `RLHFDataset`，随后写入 `data.custom_cls.name`，与 `CUSTOM_CLS_PATH` 一起动态加载数据集实现。
- **常见值**：RLHFDataset
- **来源环境变量**：CUSTOM_CLS_NAME
- **性能影响**：机制推断：类名本身无开销；被加载的数据集类可能改变样本解析、图片/多模态预处理、过滤逻辑和 dataloader CPU 开销。
- **精度影响**：机制推断：若自定义类改变 prompt 构造、label、图像字段或过滤规则，会直接改变训练/评测数据口径；类名错误会导致启动失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:8` CUSTOM_CLS_NAME=${CUSTOM_CLS_NAME:-RLHFDataset}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
