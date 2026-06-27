# actor_rollout_ref.rollout.mode

- **参数名**：`actor_rollout_ref.rollout.mode`
- **分类**：效率
- **中文解释**：选择 rollout 执行模式；Verl 源码默认 `async`，表示使用异步/server 化的 rollout 路径来承载生成请求与权重更新。
- **常见值**："async"、async
- **来源环境变量**：rollout_mode
- **性能影响**：机制推断：`async` 可让推理服务与训练调度解耦，提升资源利用和扩展性，但会增加服务进程、RPC、同步与排队管理开销。
- **精度影响**：机制推断：模式本身不改变采样分布；若异步训练造成策略滞后，需要依赖 rollout correction 等机制控制偏差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:110` actor_rollout_ref.rollout.mode=async \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:156` actor_rollout_ref.rollout.mode=${rollout_mode}
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:66` "actor_rollout_ref.rollout.mode=${rollout_mode}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
