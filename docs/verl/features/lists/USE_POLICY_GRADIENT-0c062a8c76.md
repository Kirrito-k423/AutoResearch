# USE_POLICY_GRADIENT

- **参数名**：`USE_POLICY_GRADIENT`
- **分类**：效率
- **中文解释**：文档说明：`USE_POLICY_GRADIENT` 是 examples 暴露的开关，写入 `distillation.distillation_loss.use_policy_gradient`；Verl 配置说明为 true 时把蒸馏 loss 作为 reward/策略梯度信号，为 false 时将蒸馏 loss 作为监督损失直接反传。
- **常见值**：False、True
- **来源环境变量**：USE_POLICY_GRADIENT
- **性能影响**：机制推断：会改变损失路径和需要保留/计算的 logprob 信息；源码还提示 `forward_kl_topk` 与 policy gradient 搭配时 top-k 分布信号大多无法利用。
- **精度影响**：文档说明：该开关直接改变蒸馏优化目标；Verl 源码建议 policy-gradient 模式搭配 `loss_mode=k1`，监督反传模式搭配 `k3` 或 `forward_kl_topk`。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:15` use_policy_gradient=${USE_POLICY_GRADIENT:-True}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:15` use_policy_gradient=${USE_POLICY_GRADIENT:-True}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:22` use_policy_gradient=${USE_POLICY_GRADIENT:-True}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:17` use_policy_gradient=${USE_POLICY_GRADIENT:-False}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
