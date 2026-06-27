# actor_rollout_ref.actor.use_torch_compile

- **参数名**：`actor_rollout_ref.actor.use_torch_compile`
- **分类**：效率
- **中文解释**：文档说明：控制 actor 是否使用 `torch.compile`/JIT 编译加速；官方 config 文档将其解释为 actor 侧 torch compile 开关，Ascend 参数表也标注为“是否使用 torch.compile 加速”。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：启用可能提升重复算子执行效率，但会增加编译时间和图编译/缓存开销；FAQ 建议遇到 Triton 编译错误时关闭。
- **精度影响**：机制推断：理想情况下不改变训练目标；编译后算子路径差异可能带来极小数值差异，更多风险来自编译失败导致运行中断。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：17
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:149` actor_rollout_ref.actor.use_torch_compile=False
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:70` actor_rollout_ref.actor.use_torch_compile=True
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:77` actor_rollout_ref.actor.use_torch_compile=True
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:113` actor_rollout_ref.actor.use_torch_compile=False
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:84` actor_rollout_ref.actor.use_torch_compile=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
