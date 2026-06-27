# distillation.teacher_models.gsm8k.inference.max_model_len

- **参数名**：`distillation.teacher_models.gsm8k.inference.max_model_len`
- **分类**：效率
- **中文解释**：文档说明：GSM8K 教师推理后端的最大上下文长度；OPD 文档说明 teacher `inference.max_model_len` 必须容纳 student prompt length、student response length 再加 1。
- **常见值**：$(( max_prompt_length + max_response_length + 1 ))
- **来源环境变量**：无
- **性能影响**：文档说明：该值越大，教师推理的 KV cache、显存和 prefill 时间通常越高；过小会无法覆盖蒸馏 logprob 所需序列。
- **精度影响**：文档说明：若小于所需上下文，教师 logprob 计算会失败或不完整；若上下文被截断，GSM8K 教师监督信号会失真。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:124` +distillation.teacher_models.gsm8k.inference.max_model_len=${max_num_tokens}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
