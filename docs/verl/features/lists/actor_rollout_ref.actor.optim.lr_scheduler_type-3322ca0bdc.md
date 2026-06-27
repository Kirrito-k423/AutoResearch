# actor_rollout_ref.actor.optim.lr_scheduler_type

- **参数名**：`actor_rollout_ref.actor.optim.lr_scheduler_type`
- **分类**：算法
- **中文解释**：选择 actor 优化器的学习率调度/衰减方式；VeOmni 路径会把该值传给 lr scheduler，常见语义是 `constant`、`cosine`、`linear` 或 `inverse-square-root` 一类学习率曲线。
- **常见值**：$lr_scheduler_type
- **来源环境变量**：无
- **性能影响**：机制推断：调度器本身计算开销很小，通常不影响吞吐；但不同学习率曲线会影响有效训练步数、是否需要更长 warmup/训练，以及发散后重跑成本。
- **精度影响**：文档说明：Verl optimizer config 将 `lr_scheduler_type` 作为可变字段并限制支持取值；它会改变学习率随 step 的变化，直接影响收敛速度、稳定性和最终指标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:85` actor_rollout_ref.actor.optim.lr_scheduler_type=$lr_scheduler_type \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
