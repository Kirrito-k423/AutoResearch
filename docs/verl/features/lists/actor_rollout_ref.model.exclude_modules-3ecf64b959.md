# actor_rollout_ref.model.exclude_modules

- **参数名**：`actor_rollout_ref.model.exclude_modules`
- **分类**：效率
- **中文解释**：文档说明：LoRA 配置中不应用适配器的模块匹配列表；示例用 `.*visual.*` 排除视觉相关模块，适合只给语言侧线性层加 LoRA 的 VLM 场景。
- **常见值**：'.*visual.*'
- **来源环境变量**：无
- **性能影响**：机制推断：排除模块会减少 LoRA 参数、梯度和同步/合并开销；排除范围越大，训练与权重同步越轻，但可训练容量也越小。
- **精度影响**：机制推断：排除关键模块会降低适配能力；VLM 中排除视觉模块可避免改动视觉塔，但如果任务需要视觉表征适配，可能限制最终效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh:58` actor_rollout_ref.model.exclude_modules='.*visual.*'

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
