# actor_rollout_ref.rollout.multi_stage_wake_up

- **参数名**：`actor_rollout_ref.rollout.multi_stage_wake_up`
- **分类**：效率
- **中文解释**：源码配置说明：控制 SGLang rollout engine 是否采用多阶段唤醒。Verl rollout 配置注释说明它用于训练阶段切换到 rollout 阶段时降低峰值显存，且只对 SGLang rollout 生效。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：源码配置说明：启用后可降低训练-rollout 切换时的峰值显存，减少 OOM 风险；代价是唤醒流程更分段，可能增加阶段切换延迟。
- **精度影响**：机制推断：不改变模型权重或采样参数；只有当显存压力导致 OOM、回退或 batch 调整时才会间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:109` actor_rollout_ref.rollout.multi_stage_wake_up=True
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:132` actor_rollout_ref.rollout.multi_stage_wake_up=False
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh:75` actor_rollout_ref.rollout.multi_stage_wake_up=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
