# ROLLOUT_DP

- **参数名**：`ROLLOUT_DP`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧数据并行大小，示例在 NPU 或显式覆盖时写入 `actor_rollout_ref.rollout.data_parallel_size`。
- **常见值**：未提取
- **来源环境变量**：ROLLOUT_DP
- **性能影响**：机制推断：增加 rollout DP 可并行处理更多 prompt，提高生成吞吐；也会复制模型/缓存或与 TP/EP 竞争设备资源。
- **精度影响**：机制推断：数据并行本身不改变采样分布；并行度变化可能改变样本顺序、随机种子消耗和吞吐-新鲜度，从而影响可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:34` ROLLOUT_DP=${ROLLOUT_DP:-}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
