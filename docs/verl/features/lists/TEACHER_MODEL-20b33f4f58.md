# TEACHER_MODEL

- **参数名**：`TEACHER_MODEL`
- **分类**：效率
- **中文解释**：文档说明：On-Policy Distillation 单教师示例中的教师模型路径，写入 `distillation.teacher_models.teacher_model.model_path`，用于给学生 rollout 计算教师 logprob/蒸馏信号。
- **常见值**：Qwen/Qwen3-32B、Qwen/Qwen3-VL-32B-Instruct
- **来源环境变量**：TEACHER_MODEL
- **性能影响**：机制推断：教师模型越大，显存占用、加载时间和 logprob 计算延迟越高；教师推理池可能成为 OPD 训练吞吐瓶颈。
- **精度影响**：文档说明：OPD 用冻结教师的分布作为蒸馏目标；教师模型质量和领域匹配度直接影响学生学习信号，错误或弱教师会降低蒸馏收益。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:8` TEACHER_MODEL=${TEACHER_MODEL:-Qwen/Qwen3-VL-32B-Instruct}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:8` TEACHER_MODEL=${TEACHER_MODEL:-Qwen/Qwen3-32B}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:10` TEACHER_MODEL=${TEACHER_MODEL:-Qwen/Qwen3-32B}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
