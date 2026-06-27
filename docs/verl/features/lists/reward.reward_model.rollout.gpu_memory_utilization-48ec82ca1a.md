# reward.reward_model.rollout.gpu_memory_utilization

- **参数名**：`reward.reward_model.rollout.gpu_memory_utilization`
- **分类**：算法
- **中文解释**：控制 rollout engine 可使用的显存比例，影响 KV cache 容量、吞吐和 OOM 风险。
- **常见值**：0.8
- **来源环境变量**：REWARD_ROLLOUT_GPU_MEM_UTIL
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：机制推断：直接改变 RL 目标、约束或优势估计，可能影响稳定性和最终精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:74` reward.reward_model.rollout.gpu_memory_utilization=${REWARD_ROLLOUT_GPU_MEM_UTIL}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
