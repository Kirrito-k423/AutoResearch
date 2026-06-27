# actor_rollout_ref.actor.megatron.use_remove_padding

- **参数名**：`actor_rollout_ref.actor.megatron.use_remove_padding`
- **分类**：效率
- **中文解释**：文档说明：控制 Megatron actor 训练时是否移除 padding token 后再计算；官方 config 说明 remove padding 会移除 input/response 中的 padding token，以提升模型运行效率。示例中设为 `False` 是为了强制使用 BSHD 计算格式。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：启用时通常减少无效 padding 上的注意力和 MLP 计算，提升吞吐并降低显存；关闭可换取与特定 BSHD/fused kernel 路径的兼容性，但可能浪费计算。
- **精度影响**：机制推断：正确 mask 下不应改变有效 token 的训练目标；但开启/关闭会改变 packed/unpacked 张量路径，若模型或 kernel 对 remove-padding 支持不一致，可能导致 logprob 或 mask 对齐问题。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:120` actor_rollout_ref.actor.megatron.use_remove_padding=False
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:95` actor_rollout_ref.actor.megatron.use_remove_padding=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
