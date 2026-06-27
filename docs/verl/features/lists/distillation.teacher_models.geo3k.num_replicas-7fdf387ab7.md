# distillation.teacher_models.geo3k.num_replicas

- **参数名**：`distillation.teacher_models.geo3k.num_replicas`
- **分类**：效率
- **中文解释**：文档说明：Geo3K 教师推理服务的副本数；OPD 文档说明每个 teacher 的总 GPU 占用为 `num_replicas * per_replica_world_size`，且总和必须匹配 teacher 资源池。
- **常见值**：1
- **来源环境变量**：TEACHER_NUM_REPLICAS_GEO3K
- **性能影响**：文档说明：增加副本可提升 Geo3K 教师 logprob 服务并发和吞吐，但线性占用更多 GPU；副本数与 TP/DP/PP 组合不匹配资源池会配置失败。
- **精度影响**：机制推断：副本数不改变教师模型分布；副本太少会形成瓶颈、拉大异步等待，错误资源配置会中断训练而不是改变算法目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:128` +distillation.teacher_models.geo3k.num_replicas=${TEACHER_NUM_REPLICAS_GEO3K}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
