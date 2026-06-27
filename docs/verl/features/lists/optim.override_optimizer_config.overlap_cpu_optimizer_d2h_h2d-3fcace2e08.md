# optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d

- **参数名**：`optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d`
- **分类**：效率
- **中文解释**：传给 Megatron `OptimizerConfig` 的优化器覆盖项，用于在启用 CPU optimizer/offload 时重叠 D2H/H2D 数据搬运；Verl 性能最佳实践把它列为 hybrid optimizer 的配套开关。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：与 CPU optimizer offload 一起开启可隐藏部分 GPU/CPU 传输时间，降低 offload 对 step time 的影响；也会增加调度复杂度并依赖硬件带宽。
- **精度影响**：机制推断：只改变优化器状态搬运/重叠方式，不应改变数学更新；异常同步或实现差异才可能带来数值问题。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:52` +optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:108` +optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
