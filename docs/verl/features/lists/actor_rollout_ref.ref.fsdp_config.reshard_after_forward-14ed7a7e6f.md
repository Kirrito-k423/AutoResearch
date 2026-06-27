# actor_rollout_ref.ref.fsdp_config.reshard_after_forward

- **参数名**：`actor_rollout_ref.ref.fsdp_config.reshard_after_forward`
- **分类**：效率
- **中文解释**：控制 reference model 的 FSDP 参数在前向结束后是否重新分片；`True` 表示前向后释放完整参数分片状态，后续需要时再 all-gather。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Ascend 后端特性文档将该参数描述为在内存与通信之间取舍；开启通常降低峰值显存，代价是后续重新 all-gather 的通信开销。
- **精度影响**：机制推断：仅改变参数驻留/分片策略，不改变 reference 模型计算公式；正常情况下不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:101` actor_rollout_ref.ref.fsdp_config.reshard_after_forward=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:141` actor_rollout_ref.ref.fsdp_config.reshard_after_forward=True
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:101` actor_rollout_ref.ref.fsdp_config.reshard_after_forward=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
