# distillation.distillation_loss.loss_max_clamp

- **参数名**：`distillation.distillation_loss.loss_max_clamp`
- **分类**：算法
- **中文解释**：文档说明：该参数是蒸馏 loss 的最大裁剪幅度；Verl 配置说明为 null 时不裁剪，源码会把 per-token distillation loss clamp 到 `[-loss_max_clamp, loss_max_clamp]`。
- **常见值**：10.0
- **来源环境变量**：无
- **性能影响**：机制推断：裁剪本身开销很小；主要用于抑制异常 loss/梯度峰值，减少数值不稳定导致的重试或崩溃。
- **精度影响**：机制推断：可提升训练稳定性并限制异常 token 的影响；阈值过低会削弱高损失样本的学习信号，阈值过高则保护作用变弱。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:109` distillation.distillation_loss.loss_max_clamp=10.0
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:115` distillation.distillation_loss.loss_max_clamp=10.0
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:138` distillation.distillation_loss.loss_max_clamp=10.0
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:120` distillation.distillation_loss.loss_max_clamp=10.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
