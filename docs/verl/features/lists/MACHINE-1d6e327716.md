# MACHINE

- **参数名**：`MACHINE`
- **分类**：效率
- **中文解释**：文档说明：示例脚本中的硬件标签变量；当前 `gb200` 会启用 Blackwell/SM100 相关覆盖项，例如 `enforce_eager=True`、FSDP dtype、SGLang attention backend 和 Ray GPU 数配置，未知值只进入实验名。
- **常见值**：未提取
- **来源环境变量**：MACHINE
- **性能影响**：机制推断：正确标签可选择更适合硬件的后端/调度参数，避免不兼容路径；错误标签可能导致性能下降、资源探测异常或后端不支持。
- **精度影响**：机制推断：通常不作为算法超参；但 dtype、eager/非 eager 或 attention backend 变化可能带来轻微数值差异，主要目标仍是硬件兼容和性能。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:21` MACHINE=${MACHINE:-}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
