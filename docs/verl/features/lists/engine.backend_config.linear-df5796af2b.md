# engine.backend_config.linear

- **参数名**：`engine.backend_config.linear`
- **分类**：效率
- **中文解释**：文档说明：AutoModel 普通 Linear 层后端选择，传入 `BackendConfig`；`te` 使用 TransformerEngine 线性层，`torch` 使用标准 PyTorch Linear。
- **常见值**：te
- **来源环境变量**：无
- **性能影响**：文档说明：`te` 可使用融合/低精度友好的线性层实现，通常有利于吞吐和显存带宽；需要 TransformerEngine 与硬件算子支持。
- **精度影响**：机制推断：不改变模型结构；后端 kernel 和混合精度路径不同，可能带来轻微舍入差异，需与整体 dtype/FP8 设置一致。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:42` engine.backend_config.linear=te \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
