# distillation.distillation_loss.topk

- **参数名**：`distillation.distillation_loss.topk`
- **分类**：算法
- **中文解释**：文档说明：该参数表示 top-k 蒸馏损失保留的教师候选 token 数；Verl 配置说明“若蒸馏损失需要 top-k logits，则该字段就是 K 值”，教师配置校验也要求 top-k 模式必须设置它。
- **常见值**：64
- **来源环境变量**：DISTILLATION_TOPK
- **性能影响**：机制推断：K 越大，教师 logprob 输出、Ray 传输、学生侧 gather/KL 和显存占用越大；K 越小，吞吐更好但分布信息更少。
- **精度影响**：机制推断：在 top-k 蒸馏模式下直接影响教师分布保真度；K 太小会丢失概率尾部约束，K 较大通常保留更多软标签信息但不保证单调提升。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:106` distillation.distillation_loss.topk=${distillation_topk}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:112` distillation.distillation_loss.topk=${distillation_topk}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:135` distillation.distillation_loss.topk=${distillation_topk}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:117` distillation.distillation_loss.topk=${distillation_topk}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
