# TEACHER_TP

- **参数名**：`TEACHER_TP`
- **分类**：效率
- **中文解释**：文档说明：`TEACHER_TP` 是 on-policy distillation examples 的教师推理张量并行度，写入 `distillation.teacher_models.*.inference.tensor_model_parallel_size`，用于切分教师模型推理。
- **常见值**：2
- **来源环境变量**：TEACHER_TP
- **性能影响**：机制推断：增大 TP 可降低单卡教师权重/KV 压力并支持更大教师模型，但会增加层内通信；TP 太小可能 OOM，太大可能通信瓶颈。
- **精度影响**：机制推断：通常不改变教师输出目标；只有并行后端/精度实现差异可能带来很小数值差异。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:28` teacher_tp=${TEACHER_TP:-2}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:28` teacher_tp=${TEACHER_TP:-2}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:18` teacher_tp=${TEACHER_TP:-2}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:33` teacher_tp=${TEACHER_TP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
