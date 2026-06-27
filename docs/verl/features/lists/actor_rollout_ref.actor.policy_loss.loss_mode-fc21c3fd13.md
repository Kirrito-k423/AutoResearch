# actor_rollout_ref.actor.policy_loss.loss_mode

- **参数名**：`actor_rollout_ref.actor.policy_loss.loss_mode`
- **分类**：算法
- **中文解释**：文档说明：选择 actor policy loss 的具体算法实现；examples README 将 CISPO/DPPO/GMPO/GPG/GSPO/SAPO 分别映射到对应 `loss_mode`，源码也注册了这些 loss 名称。
- **常见值**：cispo、dppo_tv、geo_mean、gpg、gspo、sapo
- **来源环境变量**：LOSS_MODE
- **性能影响**：机制推断：不同 loss 会改变 ratio、KL、序列级聚合或 correction 计算，通常相对模型前后向开销较小，但可能增加额外 logprob、聚合和指标统计开销。
- **精度影响**：文档说明：这是策略优化目标本身，直接决定 clipped objective、序列级 ratio 或算法约束；选错会把实验切到另一种训练动态。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：11
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:75` actor_rollout_ref.actor.policy_loss.loss_mode=${LOSS_MODE}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:64` actor_rollout_ref.actor.policy_loss.loss_mode=geo_mean
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:101` actor_rollout_ref.actor.policy_loss.loss_mode=gspo
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:66` actor_rollout_ref.actor.policy_loss.loss_mode=gspo
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh:73` actor_rollout_ref.actor.policy_loss.loss_mode=sapo

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
