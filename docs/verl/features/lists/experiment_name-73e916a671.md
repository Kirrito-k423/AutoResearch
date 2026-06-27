# experiment_name

- **参数名**：`experiment_name`
- **分类**：配置
- **中文解释**：脚本局部或环境可覆盖的实验名变量；示例在 router replay 脚本中根据路由重放模式和推理后端拼出名称，再传给 `trainer.experiment_name` 标识本次 run。
- **常见值**：qwen3_30b_a3b_router_replay_${ROUTING_REPLAY_MODE
- **来源环境变量**：experiment_name
- **性能影响**：机制推断：仅影响日志、tracking 和 checkpoint 目录命名，通常不改变训练吞吐；命名冲突主要影响归档、检索和恢复定位。
- **精度影响**：机制推断：不参与模型训练计算；主要影响跨 run 对比、最佳 checkpoint 管理和实验可追溯性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:69` experiment_name=${experiment_name:-qwen3_30b_a3b_router_replay_${ROUTING_REPLAY_MODE}_${INFER_BACKEND}_megatron}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
