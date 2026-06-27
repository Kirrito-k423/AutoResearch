# N_SAMPLES

- **参数名**：`N_SAMPLES`
- **分类**：效率
- **中文解释**：控制每个 prompt 生成多少条响应，增加探索和训练信号，但 rollout 成本近似线性上升。
- **常见值**：1
- **来源环境变量**：N_SAMPLES
- **性能影响**：机制推断：生成样本数越大，推理次数、输出写入和显存/KV cache 压力越高，端到端生成耗时通常近似线性增加。
- **精度影响**：机制推断：在纯生成脚本中不更新模型权重；更多样本主要增加答案多样性和评测/后处理覆盖，对模型精度无直接训练影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`

## 证据片段

- `examples/generation/run_deepseek_llm_7b.sh:25` N_SAMPLES=${N_SAMPLES:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
