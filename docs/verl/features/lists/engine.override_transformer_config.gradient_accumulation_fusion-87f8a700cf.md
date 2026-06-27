# engine.override_transformer_config.gradient_accumulation_fusion

- **参数名**：`engine.override_transformer_config.gradient_accumulation_fusion`
- **分类**：效率
- **中文解释**：文档说明：向 Megatron/MCore Transformer 配置注入梯度累积融合开关；同族 actor/ref 配置用于启用或关闭 fused gradient accumulation。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：启用融合梯度累积可减少梯度累积阶段的 kernel 调用和内存访问；关闭则更保守，常用于兼容性或问题规避。
- **精度影响**：机制推断：不改变损失定义；融合会改变部分累积顺序和 kernel 数值路径，可能产生极小浮点差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:60` +engine.override_transformer_config.gradient_accumulation_fusion=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
