# distillation.teacher_models.geo3k.inference.tensor_model_parallel_size

- **参数名**：`distillation.teacher_models.geo3k.inference.tensor_model_parallel_size`
- **分类**：效率
- **中文解释**：控制张量并行切分度，降低单卡权重/KV 压力，但会增加层内通信。
- **常见值**：2
- **来源环境变量**：TEACHER_TP
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:130` +distillation.teacher_models.geo3k.inference.tensor_model_parallel_size=${teacher_tp}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
