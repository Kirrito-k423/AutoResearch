# actor_rollout_ref.actor.megatron.override_transformer_config.deallocate_pipeline_outputs

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.deallocate_pipeline_outputs`
- **分类**：效率
- **中文解释**：文档说明：Megatron 流水线并行内存优化开关；Ascend 高级特性文档说明其作用是在张量发送到下一个 PP stage 后释放本 stage 输出数据，以降低显存峰值，默认值为 `False`。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：在 PP 场景可降低流水线激活/输出显存峰值，帮助更大模型或 batch 运行；机制上可能增加重新取数或调度复杂度，吞吐收益取决于是否由显存瓶颈主导。
- **精度影响**：机制推断：只改变中间张量生命周期，不改变计算公式；若后端实现或 PP 配置不兼容，风险表现为运行错误而不是平滑精度退化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:165` +actor_rollout_ref.actor.megatron.override_transformer_config.deallocate_pipeline_outputs=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
