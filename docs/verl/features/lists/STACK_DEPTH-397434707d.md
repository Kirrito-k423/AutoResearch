# STACK_DEPTH

- **参数名**：`STACK_DEPTH`
- **分类**：效率
- **中文解释**：控制 torch memory profiler 为每条内存分配记录保存的调用栈深度，映射到 `global_profiler.global_tool_config.torch_memory.stack_depth`；示例默认 32。
- **常见值**：32
- **来源环境变量**：STACK_DEPTH
- **性能影响**：文档说明：profiler 配置将 `stack_depth` 定义为内存分配调用栈深度；值越大，快照记录更详细，但 profiler 存储量、采集开销和分析成本更高。
- **精度影响**：机制推断：这是 profiling 元数据参数，不改变模型计算或优化目标；只可能通过额外 profiling 开销扰动性能观测。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`

## 证据片段

- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh:16` stack_depth=${STACK_DEPTH:-32}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
