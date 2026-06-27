# ray_kwargs.ray_init.num_gpus

- **参数名**：`ray_kwargs.ray_init.num_gpus`
- **分类**：效率
- **中文解释**：文档说明：传给 `ray.init(**ray_kwargs.ray_init)` 的 GPU 数量覆盖项；示例在 GB200/Docker 场景下固定 `num_gpus`，避免 Ray GPU 自动探测不准。
- **常见值**：4
- **来源环境变量**：NGPUS_PER_NODE
- **性能影响**：机制推断：决定本地 Ray runtime 暴露的 GPU 资源数量，影响 actor/rollout/ref worker 的调度与资源可见性；设置过低浪费设备，设置过高会造成调度失败或资源争用。
- **精度影响**：机制推断：不改变训练目标；资源数量变化可能改变并行度、batch 切分和随机/归约顺序，从而带来可复现性差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:83` "+ray_kwargs.ray_init.num_gpus=${NGPUS_PER_NODE}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
