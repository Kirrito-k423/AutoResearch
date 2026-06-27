# STUDENT_MODEL

- **参数名**：`STUDENT_MODEL`
- **分类**：效率
- **中文解释**：文档说明：`STUDENT_MODEL` 是 on-policy distillation examples 暴露的学生模型/HuggingFace 路径，脚本把它写入 `actor_rollout_ref.model.path`，用于指定要被训练并向教师蒸馏的 actor/student checkpoint。
- **常见值**：Qwen/Qwen3-8B、Qwen/Qwen3-VL-8B-Instruct
- **来源环境变量**：STUDENT_MODEL
- **性能影响**：机制推断：学生模型规模、架构和多模态组件直接决定训练显存、吞吐、checkpoint 加载时间以及可用并行策略；更大模型通常更慢且更吃显存。
- **精度影响**：机制推断：这是初始策略/模型能力的核心配置，直接影响蒸馏起点、可达质量和是否与数据/教师模态匹配。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:7` STUDENT_MODEL=${STUDENT_MODEL:-Qwen/Qwen3-VL-8B-Instruct}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:7` STUDENT_MODEL=${STUDENT_MODEL:-Qwen/Qwen3-8B}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:7` STUDENT_MODEL=${STUDENT_MODEL:-Qwen/Qwen3-VL-8B-Instruct}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:9` STUDENT_MODEL=${STUDENT_MODEL:-Qwen/Qwen3-8B}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
