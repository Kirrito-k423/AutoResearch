# GEN_MOE_TP

- **参数名**：`GEN_MOE_TP`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧 MoE tensor parallel 大小，示例把 `GEN_MOE_TP` 写入 `+actor_rollout_ref.rollout.moe_tensor_parallel_size`；源码配置要求该值与 `expert_parallel_size`、`tensor_model_parallel_size` 协调。
- **常见值**：2
- **来源环境变量**：GEN_MOE_TP
- **性能影响**：机制推断：增大 MoE TP 可拆分专家内部张量计算和显存压力，但会增加层内通信；源码约束中当同时设置 MoE TP 与 EP 时，两者乘积需要等于 rollout TP。
- **精度影响**：机制推断：正确并行切分通常保持等价；若 MoE TP/EP/rollout TP 不一致或后端不支持，会直接失败或造成推理侧路由/数值不一致。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:54` gen_moe_tp=${GEN_MOE_TP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
