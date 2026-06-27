# actor_rollout_ref.actor.megatron.use_megatron_fsdp

- **参数名**：`actor_rollout_ref.actor.megatron.use_megatron_fsdp`
- **分类**：效率
- **中文解释**：文档说明：Actor Megatron 后端启用 Megatron-FSDP（Zero-3 sharding）的开关。官方 Megatron-FSDP 示例通过 `actor_rollout_ref.actor.megatron.use_megatron_fsdp=True` 开启，并说明 checkpoint 会以 DTensor 形式保存到 `dist_ckpt`。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Megatron-FSDP 通过更细粒度分片降低参数、梯度和优化器状态的单卡显存，支持更大模型；代价是额外通信、reshard 以及 checkpoint 格式/保存限制。
- **精度影响**：机制推断：分片不改变优化目标；但 checkpoint 保存/加载、分布式优化器和 HF 导出路径更复杂，配置不当会影响恢复一致性或导致状态不完整。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:58` actor_rollout_ref.actor.megatron.use_megatron_fsdp=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
