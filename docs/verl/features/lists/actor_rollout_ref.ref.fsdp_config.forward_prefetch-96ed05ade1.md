# actor_rollout_ref.ref.fsdp_config.forward_prefetch

- **参数名**：`actor_rollout_ref.ref.fsdp_config.forward_prefetch`
- **分类**：效率
- **中文解释**：控制 reference model 的 FSDP forward prefetch，在当前前向计算尚未结束时预取下一次 forward all-gather。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：Verl 性能调优文档说明该开关可让 all-gather 通信与计算重叠以提升效率；只适用于 FSDP1，并可能增加短时内存/调度压力。
- **精度影响**：机制推断：只改变 FSDP 通信调度，不改变 reference logprob 的数学定义；除非触发 OOM、不同后端路径或数值异常，通常不直接影响精度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:145` actor_rollout_ref.ref.fsdp_config.forward_prefetch=False
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:142` actor_rollout_ref.ref.fsdp_config.forward_prefetch=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:127` actor_rollout_ref.ref.fsdp_config.forward_prefetch=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
