# actor_rollout_ref.actor.megatron.override_transformer_config.account_for_loss_in_pipeline_split

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.account_for_loss_in_pipeline_split`
- **分类**：算法
- **中文解释**：Megatron pipeline 切分覆盖项；Ascend 特性表说明设为 True 时，loss 层会在流水线并行的划分和放置策略中被视为一个标准 Transformer 层处理。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：该开关会改变 pipeline stage 的层数/负载分布，可能改善包含 loss 层时的 stage 均衡，也可能改变 pipeline bubble 和显存分布。
- **精度影响**：机制推断：它主要影响层放置和调度，不直接改变 loss 数学定义；可能只通过数值规约顺序或可运行的并行配置间接影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:123` +actor_rollout_ref.actor.megatron.override_transformer_config.account_for_loss_in_pipeline_split=False
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:91` +actor_rollout_ref.actor.megatron.override_transformer_config.account_for_loss_in_pipeline_split=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
