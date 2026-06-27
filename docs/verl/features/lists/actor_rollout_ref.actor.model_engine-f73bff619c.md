# actor_rollout_ref.actor.model_engine

- **参数名**：`actor_rollout_ref.actor.model_engine`
- **分类**：效率
- **中文解释**：文档说明：选择 actor 训练使用的模型引擎后端。Verl examples README 明确要求 Megatron 示例使用 `actor_rollout_ref.actor.model_engine=megatron`，engine workers 文档列出 fsdp、megatron、mindspeed、veomni 等后端到 engine class 的映射。
- **常见值**：megatron
- **来源环境变量**：无
- **性能影响**：文档说明：后端选择会改变 sharding、pipeline/tensor/context parallel、通信和 fused kernel 路径，是显存占用与吞吐的核心开关。
- **精度影响**：机制推断：目标函数不变，但不同 engine 的精度类型、融合算子和通信归约顺序可能产生细微数值差异；后端与 checkpoint 不匹配会导致加载失败或训练异常。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/scaling/run_qwen2_5_32b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:93` actor_rollout_ref.actor.model_engine=megatron
- `examples/tuning/scaling/run_qwen2_5_32b_megatron.sh:66` actor_rollout_ref.actor.model_engine=megatron

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
