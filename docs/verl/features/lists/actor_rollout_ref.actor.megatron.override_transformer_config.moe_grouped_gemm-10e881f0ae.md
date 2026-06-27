# actor_rollout_ref.actor.megatron.override_transformer_config.moe_grouped_gemm

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.moe_grouped_gemm`
- **分类**：效率
- **中文解释**：文档说明：传给 Megatron transformer config 的 MoE 优化开关，启用 grouped GEMM，把多个专家的矩阵乘更高效地组织执行。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：对 MoE 模型可减少小 GEMM 调度碎片、提升专家计算利用率和吞吐；非 MoE 或不支持 kernel 的模型收益有限。
- **精度影响**：机制推断：主要改变 MoE 计算实现方式，目标函数不变；不同 fused/grouped kernel 可能产生微小浮点舍入差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:137` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_grouped_gemm=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:167` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_grouped_gemm=True
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:101` +actor_rollout_ref.actor.megatron.override_transformer_config.moe_grouped_gemm=True

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
