# distillation.distillation_loss.use_task_rewards

- **参数名**：`distillation.distillation_loss.use_task_rewards`
- **分类**：算法
- **中文解释**：文档说明：该开关控制蒸馏训练是否同时保留任务 reward/原策略损失；源码中为 false 时会把 policy loss 置 0，只使用蒸馏 loss（系数按 1.0）更新。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：关闭任务 reward 可能减少 reward 相关计算或依赖，但教师蒸馏服务开销仍存在；开启则需要同时承担任务 reward 与蒸馏 loss 的计算/聚合。
- **精度影响**：机制推断：直接改变训练目标组成；false 更偏纯教师模仿，true 则把任务 reward 与蒸馏目标混合，可能改善任务对齐但也引入权重调参问题。
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

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:107` distillation.distillation_loss.use_task_rewards=False
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:113` distillation.distillation_loss.use_task_rewards=False
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:136` distillation.distillation_loss.use_task_rewards=False
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:118` distillation.distillation_loss.use_task_rewards=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
