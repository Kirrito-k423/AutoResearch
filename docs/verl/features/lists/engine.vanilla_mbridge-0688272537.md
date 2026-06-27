# engine.vanilla_mbridge

- **参数名**：`engine.vanilla_mbridge`
- **分类**：效率
- **中文解释**：文档说明：`engine.vanilla_mbridge` 控制 Megatron/SFT engine 使用原始 mbridge 还是 NVIDIA Megatron-Bridge；Verl 性能文档说明 true 使用 mbridge，false 使用 Megatron-Bridge，当前默认 true。
- **常见值**：False、True、True"
- **来源环境变量**：无
- **性能影响**：机制推断：主要影响 Megatron 权重转换/加载路径、模型架构兼容性和启动开销；不同 bridge 后端也可能影响支持的并行/检查点能力。
- **精度影响**：机制推断：不直接改变训练目标；若 bridge 转换不兼容或权重映射错误，会造成正确性问题，否则通常不影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:64` engine.vanilla_mbridge=True"
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:58` engine.vanilla_mbridge=False
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:61` engine.vanilla_mbridge=False
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:95` #   engine.vanilla_mbridge=True       - use mbridge (not megatron-bridge)
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:118` engine.vanilla_mbridge=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
