# ray_kwargs.ray_init.runtime_env.env_vars.TRANSFER_QUEUE_ENABLE

- **参数名**：`ray_kwargs.ray_init.runtime_env.env_vars.TRANSFER_QUEUE_ENABLE`
- **分类**：效率
- **中文解释**：文档说明：写入 Ray runtime env 的 `TRANSFER_QUEUE_ENABLE` 环境变量，用于让 Ray worker 进程感知并启用 Verl TransferQueue 数据传输/队列路径。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：文档说明：TransferQueue 旨在优化训练数据/rollout 数据在组件间的传输和排队；启用后可能改善吞吐与解耦能力，但会引入队列服务、序列化和运行时依赖。
- **精度影响**：机制推断：数据内容和算法目标不应改变；若队列顺序、丢包或环境变量与 `transfer_queue.enable` 配置不一致，可能影响样本消费顺序或导致运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh`

## 证据片段

- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh:102` +ray_kwargs.ray_init.runtime_env.env_vars.TRANSFER_QUEUE_ENABLE=1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
