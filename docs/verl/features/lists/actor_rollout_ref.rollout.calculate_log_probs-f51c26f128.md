# actor_rollout_ref.rollout.calculate_log_probs

- **参数名**：`actor_rollout_ref.rollout.calculate_log_probs`
- **分类**：效率
- **中文解释**：文档说明：控制 rollout 阶段是否同时计算并返回 log probs；官方配置默认 `false`，rollout correction 与训推一致性监控场景要求打开。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：打开后 rollout 需要额外 logprob 计算和传输，增加推理侧计算、显存或通信开销；关闭则更轻，但后续校正/监控不可用。
- **精度影响**：文档说明：Ascend 迁移指南把它作为精度监控参数；机制上不直接改变采样分布，但启用后可支持 rollout correction 或训推一致性诊断，间接帮助稳定训练。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：11
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:110` actor_rollout_ref.rollout.calculate_log_probs=True \
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:93` actor_rollout_ref.rollout.calculate_log_probs=True
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:90` actor_rollout_ref.rollout.calculate_log_probs=True
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:124` actor_rollout_ref.rollout.calculate_log_probs=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:135` actor_rollout_ref.rollout.calculate_log_probs=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
