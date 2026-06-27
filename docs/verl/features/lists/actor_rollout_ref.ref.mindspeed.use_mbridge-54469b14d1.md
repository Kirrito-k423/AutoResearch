# actor_rollout_ref.ref.mindspeed.use_mbridge

- **参数名**：`actor_rollout_ref.ref.mindspeed.use_mbridge`
- **分类**：效率
- **中文解释**：文档说明：为 reference model 的 MindSpeed 后端启用 mBridge/Megatron-Bridge 权重桥接，使 reference logprob/KL 计算能按 actor 的 MindSpeed Megatron 并行格式加载权重。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：主要增加启动、checkpoint 转换和权重同步成本；但在 MindSpeed/Megatron 格式下可避免 reference 权重加载失败，保证 KL/reference 计算链路可运行。
- **精度影响**：机制推断：正确桥接后不改变 reference 目标；若桥接切分、dtype 或权重命名不一致，会直接影响 reference logprob 和 KL 约束。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:154` actor_rollout_ref.ref.mindspeed.use_mbridge=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:165` actor_rollout_ref.ref.mindspeed.use_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
