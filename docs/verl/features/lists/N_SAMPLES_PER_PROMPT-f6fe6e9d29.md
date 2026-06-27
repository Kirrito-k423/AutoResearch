# N_SAMPLES_PER_PROMPT

- **参数名**：`N_SAMPLES_PER_PROMPT`
- **分类**：效率
- **中文解释**：控制每个 prompt 生成多少条响应，增加探索和训练信号，但 rollout 成本近似线性上升。
- **常见值**：8
- **来源环境变量**：N_SAMPLES_PER_PROMPT
- **性能影响**：机制推断：每个 prompt 生成的样本数越多，rollout 生成、奖励评估和 logprob 计算成本越高，显存与队列压力也会上升。
- **精度影响**：机制推断：更多样本增强同一 prompt 下的探索和相对比较信号，可能改善 RL 训练信号；过大则可能降低样本新鲜度或改变有效 batch 统计。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:12` n_samples_per_prompt=${N_SAMPLES_PER_PROMPT:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
