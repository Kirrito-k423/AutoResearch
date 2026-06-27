# actor_rollout_ref.actor.fsdp_config.forward_prefetch

- **参数名**：`actor_rollout_ref.actor.fsdp_config.forward_prefetch`
- **分类**：效率
- **中文解释**：文档说明：该参数控制 FSDP 训练后端是否预取下一次 forward-pass 的参数 all-gather；Verl 性能文档明确以 `actor_rollout_ref.actor.fsdp_config.forward_prefetch=True` 为例说明该开关。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：开启后可在当前 forward 计算结束前预取下一次 all-gather，让通信与计算重叠，从而改善效率；代价是更复杂的调度和潜在额外瞬时显存。
- **精度影响**：机制推断：不改变数学目标；若模型图不稳定或 FSDP 版本/后端行为不匹配，风险主要是运行正确性而非精度收益。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:150` actor_rollout_ref.actor.fsdp_config.forward_prefetch=True
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:87` actor_rollout_ref.actor.fsdp_config.forward_prefetch=False
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:122` actor_rollout_ref.actor.fsdp_config.forward_prefetch=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:69` actor_rollout_ref.actor.fsdp_config.forward_prefetch=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
