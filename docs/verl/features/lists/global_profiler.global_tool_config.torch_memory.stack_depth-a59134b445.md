# global_profiler.global_tool_config.torch_memory.stack_depth

- **参数名**：`global_profiler.global_tool_config.torch_memory.stack_depth`
- **分类**：配置
- **中文解释**：控制 profiling 采集范围和开销，用于定位耗时/显存问题，通常不直接提升精度。
- **常见值**：32
- **来源环境变量**：STACK_DEPTH
- **性能影响**：机制推断：开启 profiling 会增加采集和落盘开销。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`

## 证据片段

- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh:108` global_profiler.global_tool_config.torch_memory.stack_depth=${stack_depth}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
