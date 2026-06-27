# actor_rollout_ref.actor.fsdp_config.mixed_precision.buffer_dtype

- **参数名**：`actor_rollout_ref.actor.fsdp_config.mixed_precision.buffer_dtype`
- **分类**：效率
- **中文解释**：机制推断：FSDP mixed precision 配置中的 buffer dtype，示例在 Ascend FSDP 脚本中设为 `fp32`，用于控制模型 buffer（非参数状态，如归一化统计或其它注册 buffer）在混合精度训练中的保存/计算精度。
- **常见值**：fp32
- **来源环境变量**：无
- **性能影响**：机制推断：`fp32` buffer 比 bf16/fp16 占用更多显存和通信/拷贝带宽，但 buffer 体量通常小于参数和激活；保留 fp32 更偏稳定性取舍。
- **精度影响**：机制推断：fp32 buffer 可降低归一化或累计状态的舍入误差；改成低精度可能带来小幅数值差异，具体影响取决于模型中 buffer 的用途。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh:27` +actor_rollout_ref.actor.fsdp_config.mixed_precision.buffer_dtype=fp32 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
