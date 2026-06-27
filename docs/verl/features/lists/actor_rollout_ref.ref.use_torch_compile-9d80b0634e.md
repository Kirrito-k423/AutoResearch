# actor_rollout_ref.ref.use_torch_compile

- **参数名**：`actor_rollout_ref.ref.use_torch_compile`
- **分类**：效率
- **中文解释**：文档说明：控制 reference model 是否使用 `torch.compile`；参数表显示 ref 默认引用 actor 的 `use_torch_compile`，examples 多处显式设为 `False`。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：参数表把 `use_torch_compile` 标为加速开关；机制上启用可能提升后续前向吞吐，但会增加编译启动成本并受后端/动态图兼容性限制。
- **精度影响**：机制推断：编译应保持数值等价，通常不直接改变精度；若遇到后端不支持、图捕获差异或数值边界问题，风险体现为运行失败或微小数值差。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：10
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:158` actor_rollout_ref.ref.use_torch_compile=False
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:142` actor_rollout_ref.ref.use_torch_compile=False
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:104` actor_rollout_ref.ref.use_torch_compile=False
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:104` actor_rollout_ref.ref.use_torch_compile=False
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:142` actor_rollout_ref.ref.use_torch_compile=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
