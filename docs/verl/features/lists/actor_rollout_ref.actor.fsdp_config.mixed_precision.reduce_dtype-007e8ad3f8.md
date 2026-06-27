# actor_rollout_ref.actor.fsdp_config.mixed_precision.reduce_dtype

- **参数名**：`actor_rollout_ref.actor.fsdp_config.mixed_precision.reduce_dtype`
- **分类**：效率
- **中文解释**：文档说明：FSDP mixed precision 配置中的 reduce dtype，示例设为 `bf16`，用于控制分布式梯度/参数规约通信时采用的精度。
- **常见值**：bf16
- **来源环境变量**：无
- **性能影响**：机制推断：使用 bf16 进行 reduce 可降低通信带宽和部分显存压力，通常有利于多卡 FSDP 吞吐；收益取决于通信占比和硬件支持。
- **精度影响**：机制推断：规约精度低于 fp32 可能带来细小数值差异或稳定性风险；bf16 是大模型训练常用折中，通常比 fp16 有更大动态范围。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:89` +actor_rollout_ref.actor.fsdp_config.mixed_precision.reduce_dtype=bf16
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:71` +actor_rollout_ref.actor.fsdp_config.mixed_precision.reduce_dtype=bf16
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh:26` +actor_rollout_ref.actor.fsdp_config.mixed_precision.reduce_dtype=bf16 \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
