# actor_pp

- **参数名**：`actor_pp`
- **分类**：效率
- **中文解释**：文档说明：Actor 侧 pipeline parallel size 的脚本变量，示例中最终传给 `actor_rollout_ref.actor.megatron.pipeline_model_parallel_size`，控制 Actor Megatron 训练时把 Transformer 层切成多少个流水线 stage。
- **常见值**：6
- **来源环境变量**：actor_pp
- **性能影响**：文档说明：Verl 性能实践建议在 PP/TP/EP/ETP/CP 之间按显存和网络拓扑做平衡；增大 PP 可降低单 stage 权重/激活显存，但会引入流水线气泡和跨 stage 通信，通常在 TP 不足以容纳模型时再提高。
- **精度影响**：机制推断：不改变优化目标；只改变模型分片和调度方式。不同 PP 切分可能带来微小的浮点归约顺序差异，错误切分或与 ref/rollout 不匹配会导致运行失败或 checkpoint 不兼容。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:51` actor_pp=${actor_pp:-6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
