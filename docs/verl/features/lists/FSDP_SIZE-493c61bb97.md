# FSDP_SIZE

- **参数名**：`FSDP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：`FSDP_SIZE` 是 examples 暴露的 FSDP shard group 大小，常写入 `actor_rollout_ref.actor.fsdp_config.fsdp_size` 或 SFT `engine.fsdp_size`；Verl 配置说明 `-1` 表示使用全部可用 GPU/全局 FSDP 组。
- **常见值**：-1、16、8
- **来源环境变量**：FSDP_SIZE
- **性能影响**：机制推断：较大的 FSDP 组通常降低单卡参数/优化器状态占用，但扩大 all-gather/reduce-scatter 通信范围；较小组会形成更多 DDP x FSDP 复制分组，显存更高但通信局部性可能更好。
- **精度影响**：机制推断：不直接改变损失函数或数据；主要影响能否放下模型、batch 大小和通信稳定性，进而间接影响可训练规模。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:18` FSDP_SIZE=${FSDP_SIZE:-}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:32` fsdp_size=${FSDP_SIZE:-8}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:31` FSDP_SIZE=${FSDP_SIZE:-}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:56` fsdp_size=${FSDP_SIZE:-8}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:67` fsdp_size=${FSDP_SIZE:-16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
