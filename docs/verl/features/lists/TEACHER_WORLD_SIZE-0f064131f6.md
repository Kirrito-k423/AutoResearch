# TEACHER_WORLD_SIZE

- **参数名**：`TEACHER_WORLD_SIZE`
- **分类**：效率
- **中文解释**：文档说明：On-Policy Distillation 示例中教师资源池的每节点 GPU 数，写入 `distillation.n_gpus_per_node`，与 `distillation.nnodes` 一起决定教师池规模。
- **常见值**：4
- **来源环境变量**：TEACHER_WORLD_SIZE
- **性能影响**：文档说明：OPD 文档按 `n_gpus_per_node * nnodes` 计算教师 GPU 池，并将教师 replica 分配到连续 GPU bundle；增大该值可承载更大教师或更多副本，但占用更多资源。
- **精度影响**：机制推断：资源规模本身不改变蒸馏目标；若资源不足导致教师请求排队、失败或必须降低教师并行/上下文配置，会间接影响训练可用性和稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:12` TEACHER_WORLD_SIZE=${TEACHER_WORLD_SIZE:-4}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:12` TEACHER_WORLD_SIZE=${TEACHER_WORLD_SIZE:-4}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:14` TEACHER_WORLD_SIZE=${TEACHER_WORLD_SIZE:-4}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
