# actor_rollout_ref.actor.veomni.fsdp_size

- **参数名**：`actor_rollout_ref.actor.veomni.fsdp_size`
- **分类**：效率
- **中文解释**：源码说明：设置 VeOmni actor 的 FSDP shard group 大小，`-1` 表示使用所有可用 GPU；VeOmni engine 会据此把 data parallel 维度拆成 replicate size 与 shard size，并要求 `dp_size` 能被 `fsdp_size` 整除。
- **常见值**：$dp_size、-1
- **来源环境变量**：无
- **性能影响**：机制推断：较大的 FSDP shard group 通常降低单卡参数/优化器显存，但增加 all-gather/reduce-scatter 通信；较小分组减少通信范围但复制更多状态，占用更多显存。
- **精度影响**：机制推断：正确分片下不改变训练数学；若 `fsdp_size` 与数据并行规模不整除或与 checkpoint mesh 不匹配，会导致启动失败或状态恢复错误。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:67` actor_rollout_ref.actor.veomni.fsdp_size=$dp_size \
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:69` actor_rollout_ref.actor.veomni.fsdp_size=-1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
