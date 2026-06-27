# distillation.enabled

- **参数名**：`distillation.enabled`
- **分类**：效率
- **中文解释**：文档说明：`distillation.enabled` 控制是否启用 on-policy distillation；Verl OPD examples 将它设为 true，并额外配置教师模型、教师资源池和蒸馏损失。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：启用后需要单独的教师推理资源池，并为学生 rollout 计算教师 logprob/蒸馏 loss，增加 GPU、Ray 调度和通信开销。
- **精度影响**：文档说明：OPD 用冻结教师提供 per-token 软目标来训练学生；机制上可缩小 teacher/student gap，但会改变原 RL 目标与任务 reward 的权衡。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:97` distillation.enabled=True
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:103` distillation.enabled=True
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:113` distillation.enabled=True
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:108` distillation.enabled=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
