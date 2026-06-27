# actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_permutation_async_comm

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_permutation_async_comm`
- **分类**：效率
- **中文解释**：机制推断：MindSpeed mcore kwargs 中的 MoE token permutation 异步通信开关，用于在 MoE token 重排/反重排过程中把通信与计算尽量重叠；示例与 all-to-all dispatcher、Grouped GEMM、aux loss 负载均衡一起配置。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：开启后可隐藏 MoE token dispatch 的部分通信延迟，改善专家并行场景吞吐；同时会提高异步调度复杂度，对 HCCL/NCCL、流同步和后端实现更敏感。
- **精度影响**：机制推断：不改变路由或专家计算公式；但异步通信若同步边界处理不当会造成运行错误或难复现问题，稳定性依赖 MindSpeed 后端实现。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:143` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_permutation_async_comm=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
