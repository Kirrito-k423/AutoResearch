# actor_rollout_ref.ref.megatron.vanilla_mbridge

- **参数名**：`actor_rollout_ref.ref.megatron.vanilla_mbridge`
- **分类**：效率
- **中文解释**：文档说明：Reference Megatron 权重桥接路径选择；`True` 使用原始 mbridge，`False` 使用 NVIDIA Megatron-Bridge，本示例为 `False`。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：主要影响 Megatron 权重转换、加载、checkpoint 兼容和启动耗时；不同 bridge 对 LoRA、FSDP、MTP/并行配置的支持能力不同。
- **精度影响**：机制推断：bridge 选择本身不改变算法；若权重映射、并行切分或 dtype 转换不一致，会导致 reference logprob/KL 偏差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:76` actor_rollout_ref.ref.megatron.vanilla_mbridge=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
