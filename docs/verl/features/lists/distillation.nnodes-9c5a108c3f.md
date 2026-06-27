# distillation.nnodes

- **参数名**：`distillation.nnodes`
- **分类**：效率
- **中文解释**：文档说明：`distillation.nnodes` 是蒸馏教师资源池节点数；Verl `DistillationConfig` 会把它与 `n_gpus_per_node` 相乘得到教师资源池大小。
- **常见值**：1
- **来源环境变量**：NNODES、TEACHER_NNODES
- **性能影响**：机制推断：增加节点可扩展教师推理容量或多教师副本，但会引入跨节点调度/网络开销；资源池大小必须与教师配置匹配。
- **精度影响**：机制推断：不直接改变训练目标；间接影响来自教师请求延迟、吞吐和服务稳定性。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:99` distillation.nnodes=${NNODES}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:105` distillation.nnodes=${NNODES}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:115` distillation.nnodes=${TEACHER_NNODES}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:110` distillation.nnodes=${NNODES}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
