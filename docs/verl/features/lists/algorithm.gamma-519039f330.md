# algorithm.gamma

- **参数名**：`algorithm.gamma`
- **分类**：算法
- **中文解释**：文档说明：`algorithm.gamma` 是 RL 优势/回报计算中的折扣因子；Verl 参数表默认值为 1.0，并在 rollout correction、VeOmni GRPO 等 examples 中显式传入。
- **常见值**：$gae_gamma、1.0
- **来源环境变量**：无
- **性能影响**：机制推断：基本不影响吞吐或显存，只改变优势/回报数值计算。
- **精度影响**：机制推断：直接改变信用分配时间尺度；`gamma=1.0` 不衰减后续奖励，较小值更偏向短期奖励，可能影响长链推理任务的稳定性和最终策略。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh`
- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh`

## 证据片段

- `examples/rollout_correction/run_qwen2_5_7b_fsdp_multi_rs.sh:71` algorithm.gamma=${gamma}
- `examples/rollout_correction/run_qwen2_5_7b_fsdp.sh:68` algorithm.gamma=${gamma}
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:132` algorithm.gamma=$gae_gamma
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:127` algorithm.gamma=$gae_gamma

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
