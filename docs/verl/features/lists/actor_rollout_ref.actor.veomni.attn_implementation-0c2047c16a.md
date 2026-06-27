# actor_rollout_ref.actor.veomni.attn_implementation

- **参数名**：`actor_rollout_ref.actor.veomni.attn_implementation`
- **分类**：效率
- **中文解释**：文档说明：VeOmni actor 使用的 attention backend，Verl VeOmni 配置列出 `eager`、`sdpa`、`flash_attention_2/3`、`veomni_flash_attention_2_with_sp` 等可选实现。
- **常见值**：flash_attention_2、flash_attention_2"、veomni_flash_attention_2_with_sp
- **来源环境变量**：无
- **性能影响**：文档说明：FlashAttention/VeOmni SP attention 通常比 eager 更省显存、更高吞吐；`*_with_sp` 变体用于配合 sequence parallel，错误选择可能触发兼容性问题。
- **精度影响**：机制推断：不同 attention backend 目标等价，但 kernel 实现、融合方式和低精度计算顺序不同，可能带来微小数值差异；`eager` 更适合调试兼容性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:78` actor_rollout_ref.actor.veomni.attn_implementation=flash_attention_2 \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:70` actor_rollout_ref.actor.veomni.attn_implementation=veomni_flash_attention_2_with_sp \
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:74` actor_rollout_ref.actor.veomni.attn_implementation=flash_attention_2"

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
