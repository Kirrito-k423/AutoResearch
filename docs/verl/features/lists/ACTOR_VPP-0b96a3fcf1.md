# ACTOR_VPP

- **参数名**：`ACTOR_VPP`
- **分类**：效率
- **中文解释**：机制推断：Actor Megatron 的虚拟流水线并行大小，脚本会把它写入 `actor_rollout_ref.actor.megatron.virtual_pipeline_model_parallel_size`；当 pipeline parallel 大于 1 时用于把每个物理 stage 再切成虚拟 stage。
- **常见值**：2、null
- **来源环境变量**：ACTOR_VPP
- **性能影响**：文档说明：VPP 属于 Megatron 并行配置，主要用于降低流水线气泡、改善大模型流水线利用率；但会增加调度复杂度，并且 Ascend 文档提示 VPP 与 mbridge 同时开启存在限制。
- **精度影响**：机制推断：并行切分方式通常不改变训练目标；不合适的 VPP 可能导致启动失败、通信开销过大或数值执行顺序差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:42` actor_vpp=${ACTOR_VPP:-2}
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:63` ACTOR_VPP=${ACTOR_VPP:-null}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
