# actor_rollout_ref.actor.mindspeed.vanilla_mbridge

- **参数名**：`actor_rollout_ref.actor.mindspeed.vanilla_mbridge`
- **分类**：效率
- **中文解释**：文档说明：选择使用原始/vanilla mBridge 流程处理 MindSpeed actor 的权重桥接。Verl actor 配置注释提到在 `vanilla_mbridge=True` 且分布式文件系统可见时，可通过 mbridge 配置优化 checkpoint 保存。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响 mBridge 的转换、checkpoint 保存和跨节点文件可见性假设；在合适的分布式文件系统配置下可降低保存/同步开销，配置不当会拖慢 IO 或同步。
- **精度影响**：机制推断：桥接流程本身不应改变模型数值；但 vanilla 与非 vanilla 路径若处理权重命名、切分或保存内容不同，可能造成加载不一致。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:126` actor_rollout_ref.actor.mindspeed.vanilla_mbridge=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:131` actor_rollout_ref.actor.mindspeed.vanilla_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
