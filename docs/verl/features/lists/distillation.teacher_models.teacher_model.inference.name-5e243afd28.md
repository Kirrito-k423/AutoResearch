# distillation.teacher_models.teacher_model.inference.name

- **参数名**：`distillation.teacher_models.teacher_model.inference.name`
- **分类**：配置
- **中文解释**：机制推断：on-policy distillation 中指定教师模型的推理后端名称；示例统一设为 `vllm`，用于让教师模型通过 vLLM 执行生成或打分。
- **常见值**：vllm
- **来源环境变量**：无
- **性能影响**：机制推断：教师推理后端决定教师侧吞吐、显存占用和并行能力；`vllm` 通常用于提高批量推理效率。
- **精度影响**：机制推断：后端选择通常不改变蒸馏目标定义，但不同推理后端的采样实现、dtype 或算子细节可能带来小幅数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:102` distillation.teacher_models.teacher_model.inference.name=vllm
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:108` distillation.teacher_models.teacher_model.inference.name=vllm
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:113` distillation.teacher_models.teacher_model.inference.name=vllm

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
