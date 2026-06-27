# actor_rollout_ref.actor.megatron.override_transformer_config.account_for_embedding_in_pipeline_split

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.account_for_embedding_in_pipeline_split`
- **分类**：效率
- **中文解释**：机制推断：控制 Megatron 管线并行切分层数时是否把 embedding 层计入 pipeline split。开启后 embedding 会占用 pipeline 切分预算，影响各 PP stage 的层 offset 与首尾 stage 负载分布。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：机制推断：会改变 PP stage 的显存和计算负载分配；配置得当可缓解首段 embedding 负载或适配 checkpoint 切分，配置不均衡会增加 pipeline bubble、等待或 OOM 风险。
- **精度影响**：机制推断：不改变训练目标或采样分布；但若与 checkpoint、PP size 或层映射不一致，可能导致权重加载/层 offset 错误，进而造成训练失败或结果异常。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:122` +actor_rollout_ref.actor.megatron.override_transformer_config.account_for_embedding_in_pipeline_split=False
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:92` +actor_rollout_ref.actor.megatron.override_transformer_config.account_for_embedding_in_pipeline_split=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
