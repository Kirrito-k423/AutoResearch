# actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes

- **参数名**：`actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes`
- **分类**：效率
- **中文解释**：文档说明：rollout checkpoint engine 在训练权重同步到推理/rollout worker 时使用的权重传输 bucket 大小（MB），默认 2048，examples 常用 4096 或 6144 处理大权重。
- **常见值**：${TRTLLM_UPDATE_WEIGHTS_BUCKET_MEGABYTES:-4096}、4096、6144
- **来源环境变量**：无
- **性能影响**：文档说明：Ascend FAQ 说明单个权重张量大于 bucket 会触发断言，需把 bucket 调到大于最大权重张量；更大 bucket 可减少失败和分块压力，但占用更多缓冲内存。
- **精度影响**：机制推断：只影响权重同步的打包传输，不改变数学目标；若 bucket 太小导致同步失败或权重未更新，训练无法正常推进。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：10
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/profile/run_qwen3_8b_npu_profile_discrete.sh`
- `examples/profile/run_qwen3_8b_npu_profile_e2e.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:120` actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes=6144
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh:92` actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes=4096
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:118` actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes=4096
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:225` actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes=${TRTLLM_UPDATE_WEIGHTS_BUCKET_MEGABYTES:-4096}
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:119` actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes=4096

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
