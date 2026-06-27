# --node_rank

- **参数名**：`--node_rank`
- **分类**：效率
- **中文解释**：文档说明：多节点启动时当前节点的序号；Verl Ascend 文档也把 `node_rank` 描述为实例中的节点排序。
- **常见值**：${NODE_RANK}
- **来源环境变量**：无
- **性能影响**：机制推断：rank 编号不直接影响吞吐；错误编号会造成 rank 冲突、组网失败或数据/并行拓扑异常。
- **精度影响**：机制推断：正确 rank 下不改变训练算法；错误 rank 更可能导致启动失败，而不是产生可控精度变化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:132` --node_rank=${NODE_RANK} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
