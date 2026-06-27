# actor_rollout_ref.rollout.moe_tensor_parallel_size

- **参数名**：`actor_rollout_ref.rollout.moe_tensor_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：TensorRT-LLM rollout 专用的 MoE tensor parallel size，用于切分 MoE 专家内部张量；源码约束其只支持 `trtllm`，且与 expert parallel、rollout TP 需要协调。
- **常见值**：2
- **来源环境变量**：GEN_MOE_TP
- **性能影响**：机制推断：增大 MoE TP 可降低单卡专家计算/显存压力，但增加层内通信；源码要求同时设置 MoE TP 与 EP 时二者乘积等于 rollout `tensor_model_parallel_size`，不匹配会启动失败。
- **精度影响**：机制推断：正确并行切分通常保持推理结果等价；若 MoE TP/EP/TP 组合不一致或后端不支持，可能导致加载失败、路由不一致或数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:226` +actor_rollout_ref.rollout.moe_tensor_parallel_size=${gen_moe_tp}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
