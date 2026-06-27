# DISTILLATION_TOPK

- **参数名**：`DISTILLATION_TOPK`
- **分类**：效率
- **中文解释**：文档说明：`DISTILLATION_TOPK` 是 examples 暴露的环境变量，最终写入 `distillation.distillation_loss.topk`，表示 top-k 蒸馏损失需要保留的教师模型候选 token 数；Verl distillation 配置说明该值用于需要 top-k logits/logprobs 的蒸馏损失。
- **常见值**：64
- **来源环境变量**：DISTILLATION_TOPK
- **性能影响**：机制推断：`topk` 越大，教师侧 logprob 返回、传输、学生侧 gather/KL 计算和显存占用越高；越小则计算更轻，但教师分布信息更稀疏。
- **精度影响**：机制推断：仅在 `loss_mode` 使用 top-k 分布信号时直接影响蒸馏目标；较大的 K 能保留更多教师概率质量，较小的 K 可能削弱非采样 token 的分布约束。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:16` distillation_topk=${DISTILLATION_TOPK:-64}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:16` distillation_topk=${DISTILLATION_TOPK:-64}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:23` distillation_topk=${DISTILLATION_TOPK:-64}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:18` distillation_topk=${DISTILLATION_TOPK:-64}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
