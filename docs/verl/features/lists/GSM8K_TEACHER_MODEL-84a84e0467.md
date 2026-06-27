# GSM8K_TEACHER_MODEL

- **参数名**：`GSM8K_TEACHER_MODEL`
- **分类**：效率
- **中文解释**：机制推断：on-policy distillation 示例中的 GSM8K 文本教师模型 ID 或本地模型路径，会写入 `+distillation.teacher_models.gsm8k.model_path`，用于给数学文本数据源提供教师输出。
- **常见值**：Qwen/Qwen3-32B
- **来源环境变量**：GSM8K_TEACHER_MODEL
- **性能影响**：机制推断：教师模型规模决定推理显存、延迟和所需 teacher world size；更大的教师通常需要更多 TP/replica 资源。
- **精度影响**：机制推断：教师的数学能力和答案格式会直接影响蒸馏监督信号；更强、更匹配 GSM8K 的教师通常能提供更可靠的学生训练目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:8` GSM8K_TEACHER_MODEL=${GSM8K_TEACHER_MODEL:-Qwen/Qwen3-32B}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
