# distillation.n_gpus_per_node

- **参数名**：`distillation.n_gpus_per_node`
- **分类**：效率
- **中文解释**：文档说明：`distillation.n_gpus_per_node` 是蒸馏教师资源池每节点 GPU 数；Verl `DistillationConfig` 会用 `n_gpus_per_node * nnodes` 校验教师模型副本合计 world size。
- **常见值**：$(( (TEACHER_NUM_REPLICAS_GSM8K + TEACHER_NUM_REPLICAS_GEO3K) * teacher_tp ))、4
- **来源环境变量**：TEACHER_WORLD_SIZE
- **性能影响**：机制推断：更多教师 GPU 通常提高教师 logprob 服务并发/吞吐并支持更大教师模型，但会增加资源成本；配置与教师 replicas/TP 不一致会直接报错。
- **精度影响**：机制推断：不直接改变损失公式；通过教师服务吞吐、是否超时、是否能使用目标教师模型间接影响训练质量。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:98` distillation.n_gpus_per_node=${TEACHER_WORLD_SIZE}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:104` distillation.n_gpus_per_node=${TEACHER_WORLD_SIZE}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:114` distillation.n_gpus_per_node=${TEACHER_WORLD_SIZE}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:109` distillation.n_gpus_per_node=${TEACHER_WORLD_SIZE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
