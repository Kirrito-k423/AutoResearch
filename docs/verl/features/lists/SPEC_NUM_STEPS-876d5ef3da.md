# SPEC_NUM_STEPS

- **参数名**：`SPEC_NUM_STEPS`
- **分类**：效率
- **中文解释**：控制 SGLang + EAGLE speculative decoding 的推测步数，映射到 `actor_rollout_ref.model.mtp.speculative_num_steps`；示例默认 3。
- **常见值**：3
- **来源环境变量**：SPEC_NUM_STEPS
- **性能影响**：机制推断：步数越多，draft/verify 链路更长，接受率高时可能减少整体解码等待，接受率低时会增加额外计算和调度开销。
- **精度影响**：机制推断：若 speculative decoding 的验证逻辑严格，步数主要影响速度而非分布；过大的步数在兼容性不足或权重同步滞后时可能放大 rollout 异常风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:45` spec_num_steps=${SPEC_NUM_STEPS:-3}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
