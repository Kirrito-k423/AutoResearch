# data.output_path

- **参数名**：`data.output_path`
- **分类**：配置
- **中文解释**：生成任务写出结果的路径，`examples/generation` 通过 Hydra 追加 `+data.output_path` 保存生成后的 parquet。
- **常见值**："${OUTPUT_PATH}"
- **来源环境变量**：无
- **性能影响**：机制推断：影响结果落盘耗时和失败风险；输出目录慢、空间不足或权限错误会拖慢或中断任务。
- **精度影响**：机制推断：不改变模型生成；但下游评测读取该文件，路径写错或覆盖旧结果会影响指标可信度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`

## 证据片段

- `examples/generation/run_deepseek_llm_7b.sh:33` +data.output_path="${OUTPUT_PATH}" \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
