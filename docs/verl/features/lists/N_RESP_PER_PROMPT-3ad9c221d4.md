# N_RESP_PER_PROMPT

- **参数名**：`N_RESP_PER_PROMPT`
- **分类**：效率
- **中文解释**：控制每个 prompt 生成多少条响应，增加探索和训练信号，但 rollout 成本近似线性上升。
- **常见值**：16
- **来源环境变量**：N_RESP_PER_PROMPT
- **性能影响**：机制推断：每个 prompt 的响应数越多，rollout 生成、logprob 计算、奖励计算和缓存占用通常近似线性增加。
- **精度影响**：机制推断：更多响应可提升探索覆盖和组内相对奖励/优势估计质量，但也会改变样本分布和每步训练新鲜度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:27` n_resp_per_prompt=${N_RESP_PER_PROMPT:-16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
