# TEACHER_NUM_REPLICAS_GSM8K

- **参数名**：`TEACHER_NUM_REPLICAS_GSM8K`
- **分类**：效率
- **中文解释**：控制多教师 OPD 中 GSM8K 文本教师的副本数，映射到 `distillation.teacher_models.gsm8k.num_replicas`；总教师 GPU 需求按 `num_replicas × per_replica_world_size` 计算。
- **常见值**：1
- **来源环境变量**：TEACHER_NUM_REPLICAS_GSM8K
- **性能影响**：文档说明：OPD 文档说明每个 teacher replica 会占用其推理并行度对应的 GPU；增加 GSM8K teacher 副本可提升文本教师吞吐，但会线性增加资源占用并要求 teacher pool 大小精确匹配。
- **精度影响**：机制推断：副本数不改变教师模型或蒸馏损失；它主要影响等待时间和调度，配置不足可能拖慢训练，配置错误会导致资源校验失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:16` TEACHER_NUM_REPLICAS_GSM8K=${TEACHER_NUM_REPLICAS_GSM8K:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
