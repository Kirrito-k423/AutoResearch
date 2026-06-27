# actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_router_load_balancing_type

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_router_load_balancing_type`
- **分类**：效率
- **中文解释**：文档说明：MindSpeed mcore kwargs 中的 MoE router 负载均衡策略，示例设为 `aux_loss`，表示通过辅助负载均衡损失约束 router 分配，使 token 更均匀地落到专家上。Verl MCore config converter 中也可见 `none`、`seq_aux_loss` 等策略取值。
- **常见值**：aux_loss
- **来源环境变量**：无
- **性能影响**：机制推断：更均衡的路由可降低专家负载倾斜和 all-to-all 长尾，提升 MoE 并行效率；辅助损失本身会增加少量计算，并可能让 router 分配从纯任务最优转向负载均衡。
- **精度影响**：文档说明：Verl 的 MCore config converter 注释中将部分模型的 `moe_router_load_balancing_type` 设为 `none`，理由是 aux loss 会伤害 RL 性能；因此 `aux_loss` 可能改善负载均衡但改变训练目标，需要结合模型和指标验证。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:142` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_router_load_balancing_type=aux_loss

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
