# actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_grouped_gemm

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_grouped_gemm`
- **分类**：效率
- **中文解释**：文档说明：MindSpeed mcore kwargs 中的 MoE Grouped GEMM 开关。Ascend 高级特性文档说明 Group GEMM 用于 MoE 场景下优化专家计算，Verl NPU 安装/调优文档也将 `moe_grouped_gemm=True` 作为 MindSpeed/Megatron 相关优化项。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Grouped GEMM 将多个专家的小矩阵乘法合并/分组执行，减少 kernel launch 和提升 MoE 专家计算利用率，通常对 MoE 吞吐有利。
- **精度影响**：机制推断：矩阵乘语义不变，但分组执行会改变浮点累积顺序和低精度 kernel 路径，通常只带来微小数值差异；不支持时应关闭或回退。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:146` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_grouped_gemm=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
