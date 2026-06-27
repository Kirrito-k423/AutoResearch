# TEACHER_NNODES

- **参数名**：`TEACHER_NNODES`
- **分类**：效率
- **中文解释**：控制 on-policy distillation 中 teacher 资源池的节点数，映射到 `distillation.nnodes`；需与各 teacher 的副本数和推理并行度共同满足资源池大小约束。
- **常见值**：1
- **来源环境变量**：TEACHER_NNODES
- **性能影响**：文档说明：OPD 文档说明 teacher 资源池大小为 `n_gpus_per_node × nnodes`，且必须等于所有 teacher 的 `num_replicas × per_replica_world_size` 之和；节点数增加可扩展教师推理吞吐，但会增加 Ray 调度和跨节点通信/放置约束。
- **精度影响**：机制推断：teacher 节点数本身不改变蒸馏目标；若资源池配置不匹配会直接报错，若改变并发/调度顺序则可能带来轻微非确定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:15` TEACHER_NNODES=${TEACHER_NNODES:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
