# actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_aux_loss_coeff

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_aux_loss_coeff`
- **分类**：算法
- **中文解释**：文档说明：MindSpeed/MCore MoE 配置里的辅助负载均衡损失系数，通常与 `moe_router_load_balancing_type=aux_loss` 配合，用额外 aux loss 约束 router 更均匀地分配 token 到专家。
- **常见值**：0.001
- **来源环境变量**：无
- **性能影响**：机制推断：更均衡的专家负载可降低 MoE token dispatch/all-to-all 长尾，提升并行效率；辅助损失本身会增加少量计算，并可能改变 router 负载分布。
- **精度影响**：文档说明：相邻 `moe_router_load_balancing_type` 解释与 Verl MCore converter 注释提示 aux loss 可能影响 RL 性能；该系数越大，负载均衡约束越强，也越可能改变任务目标与最终效果。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:145` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_aux_loss_coeff=0.001

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
