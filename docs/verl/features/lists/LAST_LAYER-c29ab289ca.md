# LAST_LAYER

- **参数名**：`LAST_LAYER`
- **分类**：效率
- **中文解释**：文档说明：Megatron pipeline split 的最后流水 stage 层数，示例把 `LAST_LAYER` 写入 `num_layers_in_last_pipeline_stage`，用于在层数不能均匀切分或需要单独处理 embedding/loss stage 时手动调节。
- **常见值**：6
- **来源环境变量**：LAST_LAYER
- **性能影响**：文档说明：pipeline-parallel 调整可在层数不均时平衡 stage 负载；设置不合理会造成某些 stage 过重、pipeline bubble 增加或显存不均。
- **精度影响**：机制推断：正确拆分不改变模型数学含义；若层数配置与模型结构不匹配，可能导致初始化/加载失败，或因拓扑错误无法训练。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:41` last_layer=${LAST_LAYER:-6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
