# engine.backend_config.experts

- **参数名**：`engine.backend_config.experts`
- **分类**：效率
- **中文解释**：文档说明：AutoModel MoE expert 计算后端选择，传入 `BackendConfig`；可在 `gmm`、`torch_mm`、`torch`、`te` 等 grouped/expert matmul 实现间切换。
- **常见值**：torch_mm
- **来源环境变量**：无
- **性能影响**：文档说明：不同 expert 后端对应 grouped GEMM、PyTorch grouped matmul 或 TransformerEngine GroupedLinear，决定 MoE expert 计算吞吐、依赖包和显存/通信配合；`torch_mm` 免外部 grouped_gemm 依赖但性能需按硬件验证。
- **精度影响**：机制推断：不改变专家路由或训练目标；不同 matmul kernel、dtype 和累加路径可能产生微小数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:45` engine.backend_config.experts=torch_mm \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
