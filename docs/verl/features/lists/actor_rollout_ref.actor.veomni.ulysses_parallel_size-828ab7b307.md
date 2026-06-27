# actor_rollout_ref.actor.veomni.ulysses_parallel_size

- **参数名**：`actor_rollout_ref.actor.veomni.ulysses_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：VeOmni actor 的 Ulysses sequence parallel 并行度；示例通过 `$usp_size` 注入，并同步到 ref 的 VeOmni 配置。
- **常见值**：$usp_size
- **来源环境变量**：无
- **性能影响**：机制推断：增大该值可把长序列 attention/激活切到更多卡上，降低单卡显存并支持更长上下文；同时增加跨卡通信，过大可能降低吞吐。
- **精度影响**：机制推断：序列并行不改变模型目标；通信规约顺序变化可能带来微小数值差异，配置与 GPU 数不匹配会导致失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:76` actor_rollout_ref.actor.veomni.ulysses_parallel_size=$usp_size \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:68` actor_rollout_ref.actor.veomni.ulysses_parallel_size=$usp_size \
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:72` actor_rollout_ref.actor.veomni.ulysses_parallel_size=$usp_size \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
