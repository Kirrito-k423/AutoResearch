# engine.backend_config.attn

- **参数名**：`engine.backend_config.attn`
- **分类**：效率
- **中文解释**：文档说明：AutoModel 后端的 attention 实现选择，传入 NeMo AutoModel 的 `BackendConfig`；`te` 表示使用 TransformerEngine attention，`sdpa` 表示 PyTorch scaled dot-product attention。
- **常见值**：te
- **来源环境变量**：无
- **性能影响**：文档说明：选择 `te` 通常走融合/专用 attention kernel，可降低 attention 计算和显存开销；收益取决于 TransformerEngine、模型结构和硬件支持。
- **精度影响**：机制推断：不改变训练目标；不同 attention 后端会改变浮点计算路径，可能带来极小数值差异，若后端不兼容则可能导致运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:41` engine.backend_config.attn=te \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
