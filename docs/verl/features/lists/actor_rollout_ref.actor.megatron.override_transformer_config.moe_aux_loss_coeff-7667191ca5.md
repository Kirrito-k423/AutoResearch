# actor_rollout_ref.actor.megatron.override_transformer_config.moe_aux_loss_coeff

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_aux_loss_coeff`
- **分类**：算法
- **中文解释**：Megatron MoE transformer 覆盖项，设置 MoE auxiliary/load-balancing loss 的系数；Qwen3 VL MoE 示例注释说明 aux loss 与 z loss 用于缓解专家负载不均。
- **常见值**：0.01
- **来源环境变量**：无
- **性能影响**：机制推断：aux loss 会增加少量路由统计/辅助损失计算；更重要的是通过改善专家负载均衡，可能减少 MoE token dispatch 的长尾瓶颈。
- **精度影响**：机制推断：该系数直接改变训练目标中的 MoE 均衡正则强度；过小可能专家塌缩或负载不均，过大可能牺牲主任务优化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:134` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_aux_loss_coeff=0.01
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:115` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_aux_loss_coeff=0.01

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
