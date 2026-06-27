# actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type`
- **分类**：效率
- **中文解释**：文档说明：传给 Megatron Transformer 配置的 MoE token dispatcher 类型，控制专家路由后 token 在设备间分发/回收的通信实现；examples 使用 `alltoall` 或 `flex`。
- **常见值**：alltoall、flex
- **来源环境变量**：无
- **性能影响**：文档说明：属于官方推荐的 MoE 性能旋钮；不同 dispatcher 会改变 token dispatch 的 all-to-all 通信、buffer 组织和后端兼容性，对 MoE 大模型吞吐和通信瓶颈影响明显。
- **精度影响**：机制推断：正确实现下应保持同一专家路由语义，不直接改变目标函数；但不同通信路径可能带来非确定性顺序、数值微差或后端 bug 风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:116` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type=flex
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:85` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type=flex
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:199` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type=alltoall
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:108` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type=flex
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:113` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_token_dispatcher_type=flex

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
