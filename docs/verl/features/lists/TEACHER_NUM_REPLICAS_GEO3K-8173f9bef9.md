# TEACHER_NUM_REPLICAS_GEO3K

- **参数名**：`TEACHER_NUM_REPLICAS_GEO3K`
- **分类**：效率
- **中文解释**：控制多教师 OPD 中 Geo3K 视觉教师的副本数，映射到 `distillation.teacher_models.geo3k.num_replicas`；总教师 GPU 需求按 `num_replicas × per_replica_world_size` 计算。
- **常见值**：1
- **来源环境变量**：TEACHER_NUM_REPLICAS_GEO3K
- **性能影响**：文档说明：OPD 文档说明每个 teacher replica 会占用 `inference.tensor_model_parallel_size × data_parallel_size × pipeline_model_parallel_size` 个 GPU；副本越多，Geo3K teacher 推理并发越高，但资源占用线性增加并需满足节点放置约束。
- **精度影响**：机制推断：副本数不改变教师模型输出本身；副本不足会造成蒸馏吞吐瓶颈，副本配置错误会失败，副本间非确定性只可能间接影响样本返回顺序。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:17` TEACHER_NUM_REPLICAS_GEO3K=${TEACHER_NUM_REPLICAS_GEO3K:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
