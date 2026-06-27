# DTYPE

- **参数名**：`DTYPE`
- **分类**：效率
- **中文解释**：机制推断：Megatron/SFT 示例中的计算数据类型，写入 `engine.dtype`；常见值 `bfloat16` 用于以较低显存和更高吞吐运行大模型训练。
- **常见值**："bfloat16"、bfloat16
- **来源环境变量**：DTYPE
- **性能影响**：文档说明：bf16/fp16 下参数显存约按低精度存储，通常比 fp32 更省显存并更容易利用加速硬件；错误 dtype 可能导致算子不支持或吞吐下降。
- **精度影响**：机制推断：低精度会引入舍入误差；`bfloat16` 动态范围较大，通常比 fp16 更稳，但仍可能与 fp32 有细微数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:37` DTYPE=${DTYPE:-"bfloat16"}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:72` DTYPE=${DTYPE:-bfloat16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
