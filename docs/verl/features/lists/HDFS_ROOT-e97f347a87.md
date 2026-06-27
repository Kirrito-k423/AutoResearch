# HDFS_ROOT

- **参数名**：`HDFS_ROOT`
- **分类**：效率
- **中文解释**：文档说明：根路径变量，示例中用于拼接模型、日志或数据位置；VLM SFT 脚本用 `HDFS_ROOT` 派生 `MODEL_ID`，Verl 配置文档也保留 `default_hdfs_dir` 作为 HDFS checkpoint 路径字段。
- **常见值**：$PWD
- **来源环境变量**：HDFS_ROOT
- **性能影响**：机制推断：根路径本身不改变算子性能；若指向远程/HDFS 或慢速挂载，会影响模型加载、日志和 checkpoint 读写延迟。
- **精度影响**：机制推断：路径变量不直接影响训练目标；若它指向不同模型权重或恢复目录，会通过初始化/恢复状态改变结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:5` HDFS_ROOT=${HDFS_ROOT:-$PWD}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
