# actor_rollout_ref.actor.fsdp_config.mixed_precision.param_dtype

- **参数名**：`actor_rollout_ref.actor.fsdp_config.mixed_precision.param_dtype`
- **分类**：效率
- **中文解释**：机制推断：FSDP mixed precision 配置中的参数 dtype，示例设为 `bf16`，用于控制 Actor FSDP 训练中参数参与前向/反向计算时采用的混合精度类型。
- **常见值**：bf16
- **来源环境变量**：无
- **性能影响**：机制推断：bf16 参数计算可降低显存占用和内存带宽压力，并利用支持 bf16 的 GPU/NPU 加速；收益取决于硬件、FSDP 分片和通信占比。
- **精度影响**：机制推断：bf16 相比 fp32 有舍入误差，但动态范围较 fp16 更宽，是大模型训练常用折中；不匹配硬件或模型稳定性不足时可能影响收敛。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh:25` +actor_rollout_ref.actor.fsdp_config.mixed_precision.param_dtype=bf16 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
