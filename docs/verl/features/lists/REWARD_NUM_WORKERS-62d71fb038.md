# REWARD_NUM_WORKERS

- **参数名**：`REWARD_NUM_WORKERS`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `reward.num_workers`，控制奖励计算 worker 数；官方参数表将 `reward.num_workers` 标为奖励计算工作进程数，示例默认 8。
- **常见值**：8
- **来源环境变量**：REWARD_NUM_WORKERS
- **性能影响**：机制推断：worker 数增大可提升奖励模型/规则奖励计算并发，缓解 reward 阶段瓶颈；过大可能带来调度、显存、CPU 和队列开销。
- **精度影响**：机制推断：worker 数本身不改变奖励函数；若并发导致超时、非确定性外部工具或资源竞争，可能间接影响可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:20` REWARD_NUM_WORKERS=${REWARD_NUM_WORKERS:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
