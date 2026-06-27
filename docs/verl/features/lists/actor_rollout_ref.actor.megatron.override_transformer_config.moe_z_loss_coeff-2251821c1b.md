# actor_rollout_ref.actor.megatron.override_transformer_config.moe_z_loss_coeff

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_z_loss_coeff`
- **分类**：算法
- **中文解释**：Megatron MoE transformer 覆盖项，设置 router/logit z-loss 的系数；示例注释将 z loss 与 aux loss 一起用于缓解 MoE 专家负载不均和路由稳定性问题。
- **常见值**：0.001
- **来源环境变量**：无
- **性能影响**：机制推断：z-loss 本身只增加少量辅助损失计算；若改善路由稳定性，可能间接减少专家负载失衡带来的吞吐波动。
- **精度影响**：机制推断：该系数会正则化 MoE router logits，影响专家选择分布和训练稳定性；过强可能抑制路由表达能力，过弱可能难以稳定路由。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:135` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_z_loss_coeff=0.001
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:116` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_z_loss_coeff=0.001

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
