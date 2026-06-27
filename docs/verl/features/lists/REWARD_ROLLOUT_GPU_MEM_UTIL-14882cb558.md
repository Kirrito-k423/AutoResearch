# REWARD_ROLLOUT_GPU_MEM_UTIL

- **参数名**：`REWARD_ROLLOUT_GPU_MEM_UTIL`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `reward.reward_model.rollout.gpu_memory_utilization`，控制奖励模型 vLLM rollout/inference engine 可使用的 GPU 显存比例。
- **常见值**：0.8
- **来源环境变量**：REWARD_ROLLOUT_GPU_MEM_UTIL
- **性能影响**：文档说明：`gpu_memory_utilization` 越高，rollout 后端可用于权重/KV cache/静态内存的比例越高，通常能提升并发或承载更长序列；过高会增加 OOM 风险。
- **精度影响**：机制推断：显存比例本身不改变奖励模型分数；若设置过低导致截断、降并发、OOM 或失败重试，才会间接影响训练样本和可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:21` REWARD_ROLLOUT_GPU_MEM_UTIL=${REWARD_ROLLOUT_GPU_MEM_UTIL:-0.8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
