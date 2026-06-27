# actor_rollout_ref.actor.megatron.override_transformer_config.moe_shared_expert_overlap

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_shared_expert_overlap`
- **分类**：效率
- **中文解释**：文档说明：Megatron MoE 推荐调优项之一，用于控制共享专家相关计算/通信是否与其它 MoE 路径重叠。Verl 性能实践把它与 `moe_router_dtype`、`moe_permute_fusion`、`moe_enable_deepep`、`moe_token_dispatcher_type` 一起列为 MoE 稳定性能参数；示例中 DeepSeek V3 将其设为 `False`。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：该项属于 MoE 性能调优旋钮；开启重叠可能隐藏共享专家计算/通信延迟，关闭则更保守，常用于规避特定模型或后端的不稳定/不兼容。
- **精度影响**：机制推断：不改变 MoE 路由目标或专家权重；但异步重叠会改变执行时序，若后端实现存在同步或数值边界问题，可能影响稳定性，因此 examples 会按模型显式指定。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:114` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_shared_expert_overlap=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
