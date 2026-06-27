# engine.model_dtype

- **参数名**：`engine.model_dtype`
- **分类**：效率
- **中文解释**：文档说明：SFT/AutoModel engine 初始化或加载模型权重时使用的数据类型；配置注释支持 `fp32`、`bf16`、`fp16`，示例用 `bf16` 训练 Qwen3-30B-A3B。
- **常见值**：bf16
- **来源环境变量**：无
- **性能影响**：机制推断：`bf16`/`fp16` 相比 `fp32` 可降低参数显存和内存带宽压力，并在支持低精度 Tensor Core/NPU 算子的硬件上提升吞吐。
- **精度影响**：机制推断：会改变模型加载和计算的数值精度；`bf16` 通常适合大模型训练但仍有舍入误差，需与 optimizer master weights、混合精度策略配套。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:47` engine.model_dtype=bf16 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
