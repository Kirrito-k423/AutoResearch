# optim.override_optimizer_config.use_precision_aware_optimizer

- **参数名**：`optim.override_optimizer_config.use_precision_aware_optimizer`
- **分类**：效率
- **中文解释**：传给 Megatron `OptimizerConfig` 的优化器覆盖项，开启 precision-aware optimizer；Verl optimizer 代码会把 `override_optimizer_config` 原样并入 Megatron 优化器参数，性能文档建议它与 CPU offload 配套开启。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：该开关服务于混合精度/混合 CPU optimizer 路径，可能降低状态存储或传输压力；实际收益取决于 Megatron 优化器实现和硬件。
- **精度影响**：机制推断：会改变优化器处理低精度参数/状态的数值路径，通常用于提升混合精度稳定性，但与普通优化器可能存在收敛细节差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:53` +optim.override_optimizer_config.use_precision_aware_optimizer=True
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:109` +optim.override_optimizer_config.use_precision_aware_optimizer=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
