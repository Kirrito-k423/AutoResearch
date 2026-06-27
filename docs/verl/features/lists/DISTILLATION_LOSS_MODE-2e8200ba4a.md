# DISTILLATION_LOSS_MODE

- **参数名**：`DISTILLATION_LOSS_MODE`
- **分类**：算法
- **中文解释**：文档说明：`DISTILLATION_LOSS_MODE` 是 examples 暴露的蒸馏损失模式，写入 `distillation.distillation_loss.loss_mode`；Verl OPD README 列出 `k1`、`k3`、`forward_kl_topk` 等可选模式。
- **常见值**：forward_kl_topk、k1
- **来源环境变量**：DISTILLATION_LOSS_MODE
- **性能影响**：机制推断：`forward_kl_topk` 需要教师 top-k logprob 和学生侧 top-k KL 计算，通常比只依赖采样 token/估计器的模式更重；不同模式也会改变反传路径。
- **精度影响**：文档说明：loss mode 直接改变教师分布如何约束学生；Verl 源码建议 policy-gradient 模式搭配 `k1`，监督反传模式搭配 `k3` 或 `forward_kl_topk`。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:14` distillation_loss_mode=${DISTILLATION_LOSS_MODE:-k1}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:14` distillation_loss_mode=${DISTILLATION_LOSS_MODE:-k1}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:21` distillation_loss_mode=${DISTILLATION_LOSS_MODE:-k1}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:16` distillation_loss_mode=${DISTILLATION_LOSS_MODE:-forward_kl_topk}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
