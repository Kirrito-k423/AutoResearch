# engine.use_remove_padding

- **参数名**：`engine.use_remove_padding`
- **分类**：效率
- **中文解释**：文档说明：Megatron/SFT engine 是否移除 padding token 并使用 packed/THD 计算格式；Qwen3.5 GDN 示例显式设为 `False`，因为当时该结构在 Megatron-LM 中需要 bshd 格式。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：开启 remove padding 可减少 padding token 的无效计算并提升吞吐/显存效率；关闭会保留 bshd/padded 形态，性能较保守但兼容不支持 THD 的模型或 kernel。
- **精度影响**：机制推断：正确实现时不改变有效 token 的训练目标；若模型、attention 或 GDN kernel 不支持 packed/THD，强行开启可能导致失败或不可靠结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:16` #     - engine.use_remove_padding=False  (forces bshd compute format)
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:94` #   engine.use_remove_padding=False   - GDN requires bshd format (no THD)
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:120` engine.use_remove_padding=False \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
