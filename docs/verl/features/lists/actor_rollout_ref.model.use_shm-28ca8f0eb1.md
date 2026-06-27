# actor_rollout_ref.model.use_shm

- **参数名**：`actor_rollout_ref.model.use_shm`
- **分类**：效率
- **中文解释**：文档说明：模型加载时是否把 checkpoint 预拷贝到 `/dev/shm` 共享内存；Verl LoRA 文档将其作为推荐项以提升模型加载速度。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：`use_shm=True` 可加速本地模型加载/worker 初始化，尤其是多 worker 重复读 checkpoint 时；代价是占用 `/dev/shm` 容量，空间不足会导致加载失败。
- **精度影响**：机制推断：只改变 checkpoint 存放与读取路径，不改变权重数值；若共享内存拷贝失败或路径不一致，可能导致启动失败而不是精度变化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh:50` actor_rollout_ref.model.use_shm=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
