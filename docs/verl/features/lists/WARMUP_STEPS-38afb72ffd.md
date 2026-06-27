# WARMUP_STEPS

- **参数名**：`WARMUP_STEPS`
- **分类**：效率
- **中文解释**：控制 actor 优化器学习率预热步数，脚本传给 `actor_rollout_ref.actor.optim.lr_warmup_steps`；示例默认 0，表示不显式增加预热阶段。
- **常见值**：0
- **来源环境变量**：WARMUP_STEPS
- **性能影响**：机制推断：预热步数主要改变学习率日程，不显著改变单步计算成本；预热更长会把达到目标学习率的训练进度后移。
- **精度影响**：机制推断：学习率预热可降低训练初期大梯度/不稳定风险；设为 0 收敛更快进入目标学习率，但对大模型或长上下文任务可能增加初期不稳定风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:43` warmup_steps=${WARMUP_STEPS:-0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
