# TRACE_ALLOC_MAX_ENTRIES

- **参数名**：`TRACE_ALLOC_MAX_ENTRIES`
- **分类**：效率
- **中文解释**：控制 torch memory profiler 最多记录的内存分配条目数，映射到 `global_profiler.global_tool_config.torch_memory.trace_alloc_max_entries`；示例默认 100000。
- **常见值**：100000
- **来源环境变量**：TRACE_ALLOC_MAX_ENTRIES
- **性能影响**：文档说明：profiler 配置将其定义为最大内存分配记录数；值越大，快照更完整但内存/磁盘占用和采样开销更高，值过小可能丢失诊断信息。
- **精度影响**：机制推断：这是 profiling 采集上限，不改变模型前向/反向或优化目标；只可能通过 profiler 开销影响性能测量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`

## 证据片段

- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh:15` trace_alloc_max_entries=${TRACE_ALLOC_MAX_ENTRIES:-100000}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
