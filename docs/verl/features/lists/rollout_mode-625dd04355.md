# rollout_mode

- **参数名**：`rollout_mode`
- **分类**：效率
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.mode`，用于选择 rollout 执行模式；Verl fully async 和 Grafana/Prometheus 文档都以 `async` 作为异步 rollout/server 化路径示例。
- **常见值**：async
- **来源环境变量**：rollout_mode
- **性能影响**：机制推断：`async` 可让推理服务、请求排队和训练调度解耦，提升大模型 rollout 资源利用率；代价是服务进程、RPC、参数同步和队列管理开销上升。
- **精度影响**：机制推断：模式本身不改变采样分布；异步路径若引入策略滞后，需要配合 fully async 的同步/校正参数控制偏差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:15` rollout_mode=${rollout_mode:-async}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
