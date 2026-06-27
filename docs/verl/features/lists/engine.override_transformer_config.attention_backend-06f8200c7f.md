# engine.override_transformer_config.attention_backend

- **参数名**：`engine.override_transformer_config.attention_backend`
- **分类**：效率
- **中文解释**：覆盖 Megatron/MCore transformer 的 attention 后端；配置注释列出 `flash`、`fused`、`unfused`、`local`、`auto` 等，Ascend 文档说明 NPU/SGLang 场景常需使用 `ascend` 后端。
- **常见值**：auto
- **来源环境变量**：无
- **性能影响**：文档说明：不同 attention backend 决定使用的注意力内核；flash/TE/Ascend 等优化内核通常降低显存和延迟，错误后端可能退化、编译失败或不支持特定硬件。
- **精度影响**：机制推断：目标函数不变，但不同内核的累加顺序、mask 实现和低精度路径可能造成小幅数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:64` engine.override_transformer_config.attention_backend=auto
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:121` engine.override_transformer_config.attention_backend=auto \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
