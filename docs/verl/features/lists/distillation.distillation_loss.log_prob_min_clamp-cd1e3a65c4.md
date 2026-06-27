# distillation.distillation_loss.log_prob_min_clamp

- **参数名**：`distillation.distillation_loss.log_prob_min_clamp`
- **分类**：算法
- **中文解释**：文档说明：该参数是蒸馏损失中的 log probability 下限裁剪值；Verl 配置说明它用于在 `log q - log p` 中 p/q 接近 0 时提升稳定性，默认可为 null，examples 设为 -10.0。
- **常见值**：-10.0
- **来源环境变量**：无
- **性能影响**：机制推断：只是对 logprob 做 clamp，算量影响很小；主要作用是避免极端值带来的数值异常。
- **精度影响**：文档说明：裁剪极小 logprob 可减少爆炸 KL/梯度并提升稳定性；阈值设得过高会偏置教师/学生概率差异，削弱真实分布约束。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:110` distillation.distillation_loss.log_prob_min_clamp=-10.0
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:116` distillation.distillation_loss.log_prob_min_clamp=-10.0
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:139` distillation.distillation_loss.log_prob_min_clamp=-10.0
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:121` distillation.distillation_loss.log_prob_min_clamp=-10.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
