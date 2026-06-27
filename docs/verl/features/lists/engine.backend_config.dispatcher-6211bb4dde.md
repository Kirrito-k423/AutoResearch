# engine.backend_config.dispatcher

- **参数名**：`engine.backend_config.dispatcher`
- **分类**：效率
- **中文解释**：文档说明：AutoModel MoE token dispatcher 的实现选择，传入 `BackendConfig`；`torch` 使用标准 PyTorch 通信/本地计算路径，`deepep` 使用 DeepEP 优化的 MoE all-to-all 调度。
- **常见值**：deepep
- **来源环境变量**：无
- **性能影响**：文档说明：`deepep` 面向 MoE token dispatch 提升吞吐，尤其在 EP/MoE 规模较大时可减少调度瓶颈；同时引入 DeepEP 依赖和跨卡通信拓扑敏感性。
- **精度影响**：机制推断：dispatcher 只改变 token 在专家间的通信/调度方式，正确实现下不改变路由结果或损失；配置不匹配可能导致通信失败或训练中断。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:40` engine.backend_config.dispatcher=deepep \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
