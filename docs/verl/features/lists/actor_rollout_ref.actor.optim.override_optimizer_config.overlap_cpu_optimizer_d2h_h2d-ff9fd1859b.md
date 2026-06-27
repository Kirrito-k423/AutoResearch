# actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d

- **参数名**：`actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d`
- **分类**：效率
- **中文解释**：文档说明：Actor hybrid optimizer/CPU offload 场景下，将 CPU optimizer 的 device-to-host/host-to-device 数据传输与其他工作重叠的开关。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Verl best practices 建议与 CPU offload、precision-aware optimizer 一起开启；可隐藏部分 CPU/GPU 传输开销，但对调度和带宽更敏感。
- **精度影响**：机制推断：只改变传输/执行重叠方式，不改变优化器数学；异步重叠实现若有同步问题才会影响数值正确性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:89` +actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:122` +actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True \
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:80` +actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:139` +actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:103` +actor_rollout_ref.actor.optim.override_optimizer_config.overlap_cpu_optimizer_d2h_h2d=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
