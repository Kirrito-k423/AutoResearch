# expert_size

- **参数名**：`expert_size`
- **分类**：效率
- **中文解释**：文档说明：VeOmni MoE 示例中的 expert parallel size 环境变量，示例将其传给 `actor_rollout_ref.actor.veomni.expert_parallel_size`，用于设置专家并行规模。
- **常见值**：8
- **来源环境变量**：expert_size
- **性能影响**：机制推断：较大的 expert parallel size 可降低单 rank 承载的专家参数/计算压力，但增加 MoE token 路由、all-to-all 通信和调度复杂度。
- **精度影响**：机制推断：正确并行切分下不改变目标函数；配置与模型专家数或设备网格不匹配时会导致启动失败或训练不稳定。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:21` expert_size=${expert_size:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
