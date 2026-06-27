# reward.num_workers

- **参数名**：`reward.num_workers`
- **分类**：算法
- **中文解释**：reward 侧并发 worker 数，控制规则奖励、奖励管理器或外部 reward 执行的并行处理能力；示例默认 `8`。
- **常见值**：8
- **来源环境变量**：REWARD_NUM_WORKERS
- **性能影响**：文档说明：RewardConfig 中 `num_workers` 默认 8；增大可提升 CPU/IO 型 reward 计算并发，降低 rollout 后等待 reward 的时间，但也会增加 CPU、内存、Ray 调度或外部服务压力。
- **精度影响**：机制推断：worker 数不改变 reward 函数定义；若 reward 实现存在非确定性、共享状态、超时或顺序依赖，并发度变化可能间接影响样本得分稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:70` reward.num_workers=${REWARD_NUM_WORKERS}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
