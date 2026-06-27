# distillation.teacher_models.gsm8k.inference.name

- **参数名**：`distillation.teacher_models.gsm8k.inference.name`
- **分类**：配置
- **中文解释**：MOPD 多教师蒸馏中名为 `gsm8k` 的 teacher 推理后端名称；示例设为 `vllm`，与同一 teacher 下的 `inference.tensor_model_parallel_size`、`gpu_memory_utilization`、`max_model_len` 等配置一起决定 GSM8K teacher 如何提供蒸馏信号。
- **常见值**：vllm
- **来源环境变量**：无
- **性能影响**：文档说明：on-policy distillation 使用冻结 teacher 产生蒸馏信号；该字段选择 teacher 侧推理后端，示例为 vLLM，会影响 teacher 推理吞吐、显存占用和后端兼容性。
- **精度影响**：机制推断：后端名称本身不改变蒸馏损失公式；若不同后端在 logprob 数值、采样行为或最大长度处理上存在差异，可能间接影响 teacher 信号一致性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:121` +distillation.teacher_models.gsm8k.inference.name=vllm

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
