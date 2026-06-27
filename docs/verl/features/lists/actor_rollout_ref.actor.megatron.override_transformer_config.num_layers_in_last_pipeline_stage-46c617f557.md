# actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_last_pipeline_stage

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_last_pipeline_stage`
- **分类**：效率
- **中文解释**：文档说明：Megatron pipeline parallel 的手动切分参数，用于指定最后一个 pipeline stage 放置的 transformer 层数；Verl best practices 建议在层数不能均分时用它做 pipeline 调整。
- **常见值**：11、5、6
- **来源环境变量**：LAST_LAYER
- **性能影响**：文档说明：用于处理层数不均、embedding/loss 独立 stage 等场景，改善 pipeline 负载均衡和显存分布；错误设置会造成 stage 负载失衡、空泡增多或 OOM。
- **精度影响**：机制推断：只改变层在 pipeline stage 间的分布，通常不改变模型数学；不合法切分会导致启动失败或 checkpoint/权重映射问题。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:124` +actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_last_pipeline_stage=${last_layer}
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:110` +actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_last_pipeline_stage=11
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:131` +actor_rollout_ref.actor.megatron.override_transformer_config.num_layers_in_last_pipeline_stage=${last_layer}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
