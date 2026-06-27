# engine.backend_config.rms_norm

- **参数名**：`engine.backend_config.rms_norm`
- **分类**：效率
- **中文解释**：文档说明：AutoModel RMSNorm 层后端选择，传入 `BackendConfig`；`torch_fp32` 表示使用 PyTorch RMSNorm 并以 FP32 路径提升数值稳定性，另有 `torch`、`te` 等实现。
- **常见值**：torch_fp32
- **来源环境变量**：无
- **性能影响**：机制推断：`torch_fp32` 往往比融合低精度 RMSNorm 更保守，可能增加带宽/计算开销；`te` 等融合实现通常更快但依赖硬件和库支持。
- **精度影响**：文档说明：AutoModel 配置注释将 `torch_fp32` 标为 MoE 场景下更好的数值稳定性选择；切到低精度/融合后端可能带来舍入差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:43` engine.backend_config.rms_norm=torch_fp32 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
