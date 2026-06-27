# engine.dtype

- **参数名**：`engine.dtype`
- **分类**：效率
- **中文解释**：设置 engine 侧模型/训练计算的数据类型；Megatron/FSDP 配置中常见为 `bfloat16`，AutoModel 配置也区分 `fp32`、`bf16`、`fp16` 等权重加载或混合精度类型。
- **常见值**："bfloat16"、bfloat16
- **来源环境变量**：DTYPE
- **性能影响**：文档说明：低精度 dtype 可减少显存占用和带宽压力，并通常提升吞吐；`fp32` 更稳但更慢、更占显存，`bf16/fp16` 依赖硬件支持和算子兼容性。
- **精度影响**：机制推断：dtype 会影响数值范围和舍入误差；`bf16` 通常比 `fp16` 指数范围更稳，但相对 `fp32` 仍可能改变收敛细节。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:60` engine.dtype=${DTYPE}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:119` engine.dtype=${DTYPE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
