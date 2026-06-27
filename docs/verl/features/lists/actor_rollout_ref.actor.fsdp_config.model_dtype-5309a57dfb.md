# actor_rollout_ref.actor.fsdp_config.model_dtype

- **参数名**：`actor_rollout_ref.actor.fsdp_config.model_dtype`
- **分类**：效率
- **中文解释**：文档说明：actor FSDP 初始化/加载 Transformer 模型时使用的数据类型；examples 中常设为 `bfloat16`/`bf16` 以匹配大模型训练的低精度配置。
- **常见值**：bf16、bfloat16
- **来源环境变量**：无
- **性能影响**：机制推断：`bf16` 相比 `fp32` 可降低参数显存和内存带宽压力，并在支持 bf16 的 GPU/NPU 上提升吞吐；若硬件或算子支持不足，可能触发转换或兼容问题。
- **精度影响**：机制推断：会改变模型加载和计算的数值精度；bf16 通常保留较大指数范围、适合大模型训练，但相对 fp32 仍可能带来舍入误差，需与混合精度策略一致。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:84` actor_rollout_ref.actor.fsdp_config.model_dtype=bfloat16
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:98` +actor_rollout_ref.actor.fsdp_config.model_dtype=bfloat16
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:82` actor_rollout_ref.actor.fsdp_config.model_dtype=bfloat16
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:66` actor_rollout_ref.actor.fsdp_config.model_dtype=bfloat16
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:61` actor_rollout_ref.actor.fsdp_config.model_dtype=bf16

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
