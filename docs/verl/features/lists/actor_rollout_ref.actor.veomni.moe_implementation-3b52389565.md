# actor_rollout_ref.actor.veomni.moe_implementation

- **参数名**：`actor_rollout_ref.actor.veomni.moe_implementation`
- **分类**：效率
- **中文解释**：源码说明：选择 VeOmni actor 中 MoE 层的实现后端。Verl 的 VeOmni engine 配置注释写明该项可选 `eager` 或 `fused`，示例还使用 `fused_triton` 来走更专门的融合 MoE kernel。
- **常见值**：fused"、fused_triton
- **来源环境变量**：无
- **性能影响**：机制推断：fused/Triton MoE 实现通常减少 dispatch、combine 和专家 MLP 的中间张量与 kernel 启动开销；但依赖硬件、dtype 和模型支持，回退到 eager 更稳但通常更慢。
- **精度影响**：机制推断：语义上应等价，但不同 fused kernel 的累加顺序、精度策略和 router padding 处理可能带来小数值差异；实现不兼容会影响 MoE 路由或训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:79` actor_rollout_ref.actor.veomni.moe_implementation=fused_triton \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:71` actor_rollout_ref.actor.veomni.moe_implementation=fused"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
