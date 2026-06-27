# engine.use_megatron_fsdp

- **参数名**：`engine.use_megatron_fsdp`
- **分类**：效率
- **中文解释**：文档说明：Megatron engine 中启用 Megatron-FSDP/ZeRO-3 分片训练的开关，用于在 Megatron 并行体系下进一步分片参数和优化器状态。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：启用后可降低单卡参数/优化器显存，支撑更大模型或 batch；代价是更复杂的 all-gather/reduce-scatter 通信和 checkpoint/恢复路径。
- **精度影响**：机制推断：分片本身不改变训练目标；不同归约顺序和混合精度通信可能带来细小数值差异，配置错误会直接导致训练失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:59` engine.use_megatron_fsdp=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
