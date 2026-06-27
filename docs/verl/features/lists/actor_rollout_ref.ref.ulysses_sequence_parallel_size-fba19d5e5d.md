# actor_rollout_ref.ref.ulysses_sequence_parallel_size

- **参数名**：`actor_rollout_ref.ref.ulysses_sequence_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Reference policy 的 Ulysses sequence parallel 大小，用于把长序列维度拆到多个 rank 上执行；Verl 性能文档说明 actor、ref、critic、reward 均可设置 `ulysses_sequence_parallel_size>1`。
- **常见值**：8
- **来源环境变量**：无
- **性能影响**：文档说明：Ulysses SP 支持长序列训练/推理，降低单卡激活和 attention 压力；长序列超过 32k 时仍可能需要降低 micro batch/token limit，且 SP 会引入跨 rank 通信。
- **精度影响**：机制推断：正确 all-gather/scatter 时不改变 reference logprob；SP size 与 batch、padding/remove-padding 或模型实现不兼容时会导致形状错误或数值不一致。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:123` actor_rollout_ref.ref.ulysses_sequence_parallel_size=${sp_size}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
