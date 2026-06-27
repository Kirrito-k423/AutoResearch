# distillation.teacher_models.teacher_model.inference.max_model_len

- **参数名**：`distillation.teacher_models.teacher_model.inference.max_model_len`
- **分类**：效率
- **中文解释**：设置 on-policy distillation 中 teacher model 推理后端的最大上下文长度；应至少覆盖 student prompt length、student response length 以及额外的 teacher 计算需求。
- **常见值**：$(( max_prompt_length + max_response_length + 1 ))
- **来源环境变量**：无
- **性能影响**：文档说明：OPD 文档说明 teacher `inference.max_model_len` 必须容纳 `student_prompt_length + student_response_length + 1`；值越大，KV cache、显存和 prefill 成本通常越高。
- **精度影响**：文档说明：若该值小于所需上下文，distillation 校验会失败；若被迫截断 teacher 上下文，则会影响教师监督信号。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:104` distillation.teacher_models.teacher_model.inference.max_model_len=${max_num_tokens}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:110` distillation.teacher_models.teacher_model.inference.max_model_len=${max_num_tokens}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:115` distillation.teacher_models.teacher_model.inference.max_model_len=${max_num_tokens}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
