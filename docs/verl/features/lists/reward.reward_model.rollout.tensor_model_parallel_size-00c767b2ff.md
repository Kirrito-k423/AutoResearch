# reward.reward_model.rollout.tensor_model_parallel_size

- **参数名**：`reward.reward_model.rollout.tensor_model_parallel_size`
- **分类**：算法
- **中文解释**：控制张量并行切分度，降低单卡权重/KV 压力，但会增加层内通信。
- **常见值**：1
- **来源环境变量**：REWARD_ROLLOUT_TP
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：机制推断：直接改变 RL 目标、约束或优势估计，可能影响稳定性和最终精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:75` reward.reward_model.rollout.tensor_model_parallel_size=${REWARD_ROLLOUT_TP}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
