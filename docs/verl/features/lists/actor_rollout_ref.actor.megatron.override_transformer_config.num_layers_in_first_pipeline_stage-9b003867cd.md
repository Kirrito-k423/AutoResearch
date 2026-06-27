# actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_first_pipeline_stage

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_first_pipeline_stage`
- **分类**：效率
- **中文解释**：源码说明：指定 Megatron 不均匀 pipeline parallelism 中第一个 PP stage 承载的 transformer 层数。Verl 的 Megatron 工具会用它从总层数中扣除首段层数，再为中间 stage 计算层 offset。
- **常见值**：11、5
- **来源环境变量**：无
- **性能影响**：机制推断：用于平衡首段 embedding/视觉模块/路由开销与 transformer 层计算；合适取值可改善 PP 负载均衡，错误取值会造成某些 stage 过载、pipeline 空泡或显存压力。
- **精度影响**：机制推断：不改变模型数学结构；但必须与 checkpoint 分片和 pipeline 配置一致，否则可能出现层权重映射错误或启动校验失败。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:109` +actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_first_pipeline_stage=11
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:130` +actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_first_pipeline_stage=${first_layer}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
