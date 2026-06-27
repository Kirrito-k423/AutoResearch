# actor_rollout_ref.hybrid_engine

- **参数名**：`actor_rollout_ref.hybrid_engine`
- **分类**：效率
- **中文解释**：文档说明：控制 Actor/Rollout/Ref 是否作为混合 worker/colocated worker 运行；普通 RayPPOTrainer 当前断言只支持 hybrid engine，而 fully-async split-placement 示例会设为 `False` 以拆分训练与 rollout 资源池。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：hybrid/colocation 的主要收益是 actor 与 rollout 共址后可用 NCCL 快速同步权重，LoRA PPO 中 actor/ref 共址也能复用 base model；fully-async 关闭它可做训练/rollout 分离调度，但会引入异步同步和资源编排成本。
- **精度影响**：机制推断：worker 放置方式本身不改变算法；fully-async 或 one-step-off 布局会引入参数同步滞后，需要用 staleness/同步阈值控制 off-policy 影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:84` actor_rollout_ref.hybrid_engine=False \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
