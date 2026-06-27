# actor_rollout_ref.actor.megatron.dtype

- **参数名**：`actor_rollout_ref.actor.megatron.dtype`
- **分类**：效率
- **中文解释**：文档说明：Megatron 训练引擎使用的数据类型，示例多设为 `bfloat16`，需要与大模型混合精度训练配置保持一致。
- **常见值**："bfloat16"、bfloat16
- **来源环境变量**：无
- **性能影响**：机制推断：bf16 相比 fp32 降低显存和带宽需求，并可利用硬件低精度矩阵计算提升吞吐；硬件不支持时可能收益下降或不可用。
- **精度影响**：机制推断：bf16 不是完全 fp32 精度，可能引入数值差异；但动态范围较大，是大模型训练常用的稳定混合精度选择。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:89` actor_rollout_ref.actor.megatron.dtype=${dtype}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:129` actor_rollout_ref.actor.megatron.dtype=bfloat16
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:93` actor_rollout_ref.actor.megatron.dtype=bfloat16

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
