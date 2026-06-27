# distillation.distillation_loss.use_policy_gradient

- **参数名**：`distillation.distillation_loss.use_policy_gradient`
- **分类**：算法
- **中文解释**：文档说明：该开关决定蒸馏 loss 是否作为 policy-gradient reward 进入 PPO 风格损失；关闭时，蒸馏 loss 作为监督损失直接反向传播。
- **常见值**：False、True
- **来源环境变量**：USE_POLICY_GRADIENT
- **性能影响**：机制推断：会改变损失组合和反传路径；源码提示 `forward_kl_topk` 在 policy-gradient 模式下大部分 top-k 分布信号无法被利用，因此该组合可能性价比较低。
- **精度影响**：文档说明：直接改变蒸馏信号进入优化的方式；policy-gradient 模式更贴近 reward shaping，监督模式更直接拟合教师分布，二者稳定性和偏差不同。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:108` distillation.distillation_loss.use_policy_gradient=${use_policy_gradient}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:114` distillation.distillation_loss.use_policy_gradient=${use_policy_gradient}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:137` distillation.distillation_loss.use_policy_gradient=${use_policy_gradient}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:119` distillation.distillation_loss.use_policy_gradient=${use_policy_gradient}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
