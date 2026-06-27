# actor_rollout_ref.rollout.layered_summon

- **参数名**：`actor_rollout_ref.rollout.layered_summon`
- **分类**：效率
- **中文解释**：LoRA + FSDP 场景下同步 rollout 权重时按层 gather FSDP shard，主要用于把 LoRA adapter 同步到 vLLM，要求 base model 已在 vLLM 侧预加载。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Verl LoRA 文档推荐大模型或显存紧张时开启，以降低同步 LoRA 到 vLLM 的 GPU 峰值显存；代价是更细粒度 gather 带来的同步调度开销。
- **精度影响**：机制推断：只改变权重同步方式，不改变 adapter 数值；正常同步成功时不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:80` actor_rollout_ref.rollout.layered_summon=True
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh:77` actor_rollout_ref.rollout.layered_summon=True
- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh:75` actor_rollout_ref.rollout.layered_summon=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
