# actor_rollout_ref.actor.megatron.vanilla_mbridge

- **参数名**：`actor_rollout_ref.actor.megatron.vanilla_mbridge`
- **分类**：效率
- **中文解释**：文档说明：在 `use_mbridge=True` 时选择具体权重转换路径；`True` 使用 mbridge，`False` 使用 NVIDIA Megatron-Bridge。官方最佳实践说明当前默认 True，后续版本计划转向 False。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响 Megatron 权重转换、checkpoint 兼容和启动/恢复流程；机制推断：稳定训练 step 吞吐通常不由该开关直接决定，但错误组合会导致初始化失败或额外转换开销。
- **精度影响**：机制推断：转换正确时不应改变权重数值语义；转换路径不兼容、VPP/QAT 等限制未满足时，可能加载错误或直接失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:151` actor_rollout_ref.actor.megatron.vanilla_mbridge=False
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:119` actor_rollout_ref.actor.megatron.vanilla_mbridge=True
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:196` actor_rollout_ref.actor.megatron.vanilla_mbridge=False
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:57` actor_rollout_ref.actor.megatron.vanilla_mbridge=False
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:83` actor_rollout_ref.actor.megatron.vanilla_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
