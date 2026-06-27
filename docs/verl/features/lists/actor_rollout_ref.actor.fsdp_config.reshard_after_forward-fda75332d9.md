# actor_rollout_ref.actor.fsdp_config.reshard_after_forward

- **参数名**：`actor_rollout_ref.actor.fsdp_config.reshard_after_forward`
- **分类**：效率
- **中文解释**：文档说明：FSDP 配置项，控制 forward 后是否重新切分/reshard 参数；Verl FSDP 配置注释说明它用于降低内存占用。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：开启会在 forward 后释放完整参数副本、降低峰值显存，但后续阶段可能增加 all-gather/reshard 通信；关闭可减少通信但显存占用更高。
- **精度影响**：机制推断：只改变参数驻留和通信时机，通常不改变数学目标；OOM、通信失败或不同精度通信路径可能间接影响稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:88` actor_rollout_ref.actor.fsdp_config.reshard_after_forward=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:117` actor_rollout_ref.actor.fsdp_config.reshard_after_forward=True
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:88` actor_rollout_ref.actor.fsdp_config.reshard_after_forward=True

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
