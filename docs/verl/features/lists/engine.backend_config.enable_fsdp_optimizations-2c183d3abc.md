# engine.backend_config.enable_fsdp_optimizations

- **参数名**：`engine.backend_config.enable_fsdp_optimizations`
- **分类**：效率
- **中文解释**：文档说明：AutoModel `BackendConfig` 中的 FSDP 优化开关，用于在 AutoModel + FSDP2 路径启用后端侧的 FSDP 专用优化。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：启用后可让 AutoModel 后端采用更适合 FSDP 的包装、通信或状态处理路径，目标是降低 FSDP 训练的调度/显存开销；实际收益依赖模型和 FSDP2 配置。
- **精度影响**：机制推断：属于执行效率优化，不改变 loss 或优化器超参；不同分片和通信时序可能带来细小浮点归约差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:44` engine.backend_config.enable_fsdp_optimizations=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
