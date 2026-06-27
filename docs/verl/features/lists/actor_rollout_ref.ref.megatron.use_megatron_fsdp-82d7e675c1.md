# actor_rollout_ref.ref.megatron.use_megatron_fsdp

- **参数名**：`actor_rollout_ref.ref.megatron.use_megatron_fsdp`
- **分类**：效率
- **中文解释**：机制推断：Reference Megatron engine 是否启用 Megatron-FSDP/ZeRO-3 风格参数分片；配置文件说明该开关用于 Megatron-FSDP sharding。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：可显著降低 ref 模型单卡参数显存，支持更大模型；代价是参数 all-gather/reshard 通信和更复杂的 checkpoint/bridge 路径。
- **精度影响**：机制推断：正确分片时不改变 reference 计算；若 sharding、dtype 或 bridge 映射配置错误，会直接影响 ref logprob/KL 正确性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:77` actor_rollout_ref.ref.megatron.use_megatron_fsdp=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
