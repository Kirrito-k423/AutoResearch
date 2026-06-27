# actor.use_prefix_grouper

- **参数名**：`actor.use_prefix_grouper`
- **分类**：效率
- **中文解释**：文档说明：启用 PrefixGrouper 前缀分组优化；示例文件名使用短参数名 `actor.use_prefix_grouper`，实际训练配置位于 `actor_rollout_ref.actor.use_prefix_grouper=True`。开启后 Verl 会为 attention 函数注入 `prefix_grouper` 参数，并在 batch balance 时尽量把同一 `uid` 的样本放在同一 DP rank，便于共享前缀计算。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：PrefixGrouper 示例 README 给出 Qwen3-4B、4×H800 benchmark，4K/8K 场景下 old_log_prob、update_actor 和 step 均有加速；上下文越长收益越明显。机制上会增加分组调度约束，batch 中 uid 组数需要能被 DP size 整除。
- **精度影响**：机制推断：不改变损失函数或采样分布，主要改变 attention 计算路径和 batch 重排；同一前缀分组有助于保持共享前缀样本同 rank 处理，但若 uid/批大小配置不满足约束会直接报错而不是产生隐式精度变化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/prefix_grouper/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/prefix_grouper/run_qwen3_8b_fsdp.sh:3` # Demonstrates `actor.use_prefix_grouper=True` on Qwen3-8B / GSM8K.

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
