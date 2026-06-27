# critic.forward_max_token_len_per_gpu

- **参数名**：`critic.forward_max_token_len_per_gpu`
- **分类**：效率
- **中文解释**：文档说明：critic 前向计算时每 GPU 允许处理的最大 token 数；参数表说明默认引用 `critic.ppo_max_token_len_per_gpu`。
- **常见值**：8192
- **来源环境变量**：无
- **性能影响**：机制推断：上限越大，critic 前向可用更大的动态 batch/token 块，可能提高吞吐但增加激活显存；上限较小可降低 OOM 风险，但可能增加切分次数和调度开销。
- **精度影响**：机制推断：在不截断样本且计算等价时不直接影响价值函数目标；若设置过低导致长序列无法处理、频繁失败或被迫调整长度，才会间接影响训练质量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:86` critic.forward_max_token_len_per_gpu=8192 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
