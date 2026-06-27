# actor_rollout_ref.actor.veomni.enable_full_shard

- **参数名**：`actor_rollout_ref.actor.veomni.enable_full_shard`
- **分类**：效率
- **中文解释**：文档说明：VeOmni/FSDP 训练中启用 full shard（ZeRO-3 风格）的开关；Verl 配置说明该项用于 fully shard FSDP training。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：full shard 会切分参数、梯度和优化器状态以显著降低单卡显存，从而训练更大模型；代价是更多 all-gather/reduce-scatter 通信和调度开销。
- **精度影响**：机制推断：只改变状态分片和通信方式，通常不改变训练目标；低精度通信或通信时序差异可能带来极小数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:75` actor_rollout_ref.actor.veomni.enable_full_shard=True \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:66` actor_rollout_ref.actor.veomni.enable_full_shard=True \
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:71` actor_rollout_ref.actor.veomni.enable_full_shard=True \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
