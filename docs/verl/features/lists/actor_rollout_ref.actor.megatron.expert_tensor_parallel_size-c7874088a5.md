# actor_rollout_ref.actor.megatron.expert_tensor_parallel_size

- **参数名**：`actor_rollout_ref.actor.megatron.expert_tensor_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Megatron MoE expert tensor parallel 的切分度，用于进一步拆分专家内部张量计算，常与 expert/model parallel、TP、PP 和 ref 侧并行配置保持一致。
- **常见值**：$ETP、1、4
- **来源环境变量**：ACTOR_ETP、ETP
- **性能影响**：文档说明：ETP 可降低单卡专家计算/参数压力，但增加专家内部张量通信；需要结合 MoE 路由、网络拓扑和显存约束调优。
- **精度影响**：机制推断：正确切分不改变训练目标；与 checkpoint 或 ref 侧并行设置不一致会造成加载/同步失败风险。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：13
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:89` actor_rollout_ref.actor.megatron.expert_tensor_parallel_size=${actor_etp}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:80` actor_rollout_ref.actor.megatron.expert_tensor_parallel_size=${actor_etp}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:106` actor_rollout_ref.actor.megatron.expert_tensor_parallel_size=${actor_etp}
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:65` actor_rollout_ref.actor.megatron.expert_tensor_parallel_size=${ACTOR_ETP}
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:147` actor_rollout_ref.actor.megatron.expert_tensor_parallel_size=$ETP

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
