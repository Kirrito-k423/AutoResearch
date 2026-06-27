# actor_rollout_ref.actor.fsdp_config.fsdp_size

- **参数名**：`actor_rollout_ref.actor.fsdp_config.fsdp_size`
- **分类**：效率
- **中文解释**：文档说明：控制 actor FSDP 分片组大小；`-1` 表示按可用 world size 自动/整体分片，正数表示每个 FSDP shard group 使用的设备数。
- **常见值**：-1、16、8
- **来源环境变量**：FSDP_SIZE
- **性能影响**：文档说明：决定 FSDP device mesh 和 ZeRO/FSDP 分片范围；更大的分片组通常降低单卡参数/优化器显存，但增加 all-gather/reduce-scatter 通信，小分片组可能更快但显存压力更高。
- **精度影响**：机制推断：理论上不改变训练目标；不同分片/归约顺序可能带来细小浮点差异，主要影响是能否容纳目标模型和 batch。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:88` actor_rollout_ref.actor.fsdp_config.fsdp_size=-1
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:87` actor_rollout_ref.actor.fsdp_config.fsdp_size=${fsdp_size}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:116` actor_rollout_ref.actor.fsdp_config.fsdp_size=${fsdp_size}
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:87` actor_rollout_ref.actor.fsdp_config.fsdp_size=${fsdp_size}
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:70` actor_rollout_ref.actor.fsdp_config.fsdp_size=-1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
