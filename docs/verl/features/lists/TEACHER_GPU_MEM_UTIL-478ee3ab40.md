# TEACHER_GPU_MEM_UTIL

- **参数名**：`TEACHER_GPU_MEM_UTIL`
- **分类**：效率
- **中文解释**：文档说明：`TEACHER_GPU_MEM_UTIL` 是 on-policy distillation examples 的教师推理显存比例，写入 `distillation.teacher_models.*.inference.gpu_memory_utilization`，控制教师 rollout/inference engine 可使用的 GPU 显存上限。
- **常见值**：0.4
- **来源环境变量**：TEACHER_GPU_MEM_UTIL
- **性能影响**：机制推断：值越高通常可容纳更多 KV cache、并发或更长上下文，提高教师 logprob 服务吞吐，但 OOM 风险增加；值过低会浪费显存并限制并发。
- **精度影响**：机制推断：不直接改变教师分布或学生损失；若显存过低导致上下文长度、batch 或服务稳定性受限，才会间接影响训练数据质量。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:29` teacher_gpu_mem_util=${TEACHER_GPU_MEM_UTIL:-0.4}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:29` teacher_gpu_mem_util=${TEACHER_GPU_MEM_UTIL:-0.4}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:35` teacher_gpu_mem_util=${TEACHER_GPU_MEM_UTIL:-0.4}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:34` teacher_gpu_mem_util=${TEACHER_GPU_MEM_UTIL:-0.4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
