# distillation.distillation_loss.loss_mode

- **参数名**：`distillation.distillation_loss.loss_mode`
- **分类**：算法
- **中文解释**：文档说明：该参数选择蒸馏损失函数模式；Verl OPD README 列出 `k1`、`k3`、`forward_kl_topk` 等模式，源码会据此加载对应 loss settings。
- **常见值**：forward_kl_topk、k1
- **来源环境变量**：DISTILLATION_LOSS_MODE
- **性能影响**：机制推断：选择 top-k KL 模式会增加教师 top-k logprob 请求、传输和学生侧 gather/KL 计算；非 top-k 模式通常更轻，但信号形式不同。
- **精度影响**：文档说明：该字段直接决定蒸馏目标的数学形式；源码对 `use_policy_gradient` 与 `loss_mode` 的组合给出建议和告警，说明组合会影响可利用的教师信号。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:105` distillation.distillation_loss.loss_mode=${distillation_loss_mode}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:111` distillation.distillation_loss.loss_mode=${distillation_loss_mode}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:134` distillation.distillation_loss.loss_mode=${distillation_loss_mode}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:116` distillation.distillation_loss.loss_mode=${distillation_loss_mode}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
