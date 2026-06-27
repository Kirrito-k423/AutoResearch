# ROLLOUT_BATCH_SIZE

- **参数名**：`ROLLOUT_BATCH_SIZE`
- **分类**：效率
- **中文解释**：机制推断：MTP RL 示例中的 rollout/prompt batch size，脚本将其写入 `data.train_batch_size`，控制每轮训练收集和处理的 prompt 批量。
- **常见值**：32
- **来源环境变量**：ROLLOUT_BATCH_SIZE
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：更大的 batch 可降低梯度/优势估计方差并提高样本覆盖，但也会改变每步更新频率和样本新鲜度；过小可能训练噪声更大。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:11` rollout_batch_size=${ROLLOUT_BATCH_SIZE:-32}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
