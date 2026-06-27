# GEO3K_TEACHER_MODEL

- **参数名**：`GEO3K_TEACHER_MODEL`
- **分类**：效率
- **中文解释**：机制推断：on-policy distillation 示例中的 Geo3K/VL 教师模型 ID 或本地模型路径，会写入 `+distillation.teacher_models.geo3k.model_path`，用于给几何/多模态数据源提供教师输出。
- **常见值**：Qwen/Qwen3-VL-32B-Instruct
- **来源环境变量**：GEO3K_TEACHER_MODEL
- **性能影响**：机制推断：教师模型越大、上下文越长，教师推理显存和延迟越高；还会影响教师 replica、TP 和 GPU 显存利用率的资源需求。
- **精度影响**：机制推断：教师模型能力、领域匹配和输出质量会直接影响蒸馏目标；换成更弱或不匹配的教师可能降低学生在 Geo3K/VL 任务上的表现。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:9` GEO3K_TEACHER_MODEL=${GEO3K_TEACHER_MODEL:-Qwen/Qwen3-VL-32B-Instruct}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
