# ep_size

- **参数名**：`ep_size`
- **分类**：效率
- **中文解释**：文档说明：VeOmni MoE 示例中的 expert parallel size 环境变量，后续写入 `actor_rollout_ref.actor.veomni.expert_parallel_size`，控制专家并行维度大小。
- **常见值**：1
- **来源环境变量**：ep_size
- **性能影响**：机制推断：增大 EP 可分摊 MoE 专家权重和专家计算，但会增加 token dispatch/all-to-all 通信与负载均衡压力；需要与 TP、FSDP/DP 和硬件拓扑匹配。
- **精度影响**：机制推断：专家并行切分不直接改变算法目标；若并行配置导致专家负载不均、通信错误或 OOM，才会间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:19` ep_size=${ep_size:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
