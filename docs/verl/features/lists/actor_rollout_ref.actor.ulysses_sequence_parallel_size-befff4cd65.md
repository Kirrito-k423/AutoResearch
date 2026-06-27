# actor_rollout_ref.actor.ulysses_sequence_parallel_size

- **参数名**：`actor_rollout_ref.actor.ulysses_sequence_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Actor 的 Ulysses sequence parallel 并行度；Verl 性能文档说明长上下文训练可将 `ulysses_sequence_parallel_size>1` 设置在 actor/ref/critic/reward 上。
- **常见值**：2、4、8
- **来源环境变量**：无
- **性能影响**：文档说明：Ulysses 序列并行把长序列维度切到多卡以降低激活和 attention 显存，支持更长上下文；同时会增加序列并行通信，吞吐收益依赖序列长度和网络。
- **精度影响**：机制推断：并行切分不改变训练目标；通信规约和 kernel 顺序可能带来微小数值差异，配置不当则可能 OOM 或报错。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh`

## 证据片段

- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh:70` actor_rollout_ref.actor.ulysses_sequence_parallel_size=2
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:81` actor_rollout_ref.actor.ulysses_sequence_parallel_size=${sp_size}
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh:24` actor_rollout_ref.actor.ulysses_sequence_parallel_size=4 \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
