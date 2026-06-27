# actor_rollout_ref.actor.veomni.expert_parallel_size

- **参数名**：`actor_rollout_ref.actor.veomni.expert_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：该参数是 VeOmni actor 的 MoE expert parallel size；Verl VeOmni engine 配置默认值为 1，源码会把它作为额外并行维度初始化。
- **常见值**：$ep_size、$expert_size、1
- **来源环境变量**：无
- **性能影响**：机制推断：增大专家并行可分摊 MoE 专家权重和 token dispatch 负载，但会增加专家路由/all-to-all 通信；需要与 TP、FSDP/DP、硬件拓扑匹配。
- **精度影响**：机制推断：不直接改变算法目标；如果专家并行配置影响负载均衡、溢出或运行稳定性，才会间接影响训练质量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:77` actor_rollout_ref.actor.veomni.expert_parallel_size=$expert_size \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:69` actor_rollout_ref.actor.veomni.expert_parallel_size=$ep_size \
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:70` actor_rollout_ref.actor.veomni.expert_parallel_size=1
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:73` actor_rollout_ref.actor.veomni.expert_parallel_size=1 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
