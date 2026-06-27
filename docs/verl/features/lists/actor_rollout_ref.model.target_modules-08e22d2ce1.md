# actor_rollout_ref.model.target_modules

- **参数名**：`actor_rollout_ref.model.target_modules`
- **分类**：效率
- **中文解释**：文档说明：LoRA 要注入 adapter 的目标模块；FSDP LoRA 通常设为 `all-linear`，Megatron LoRA 可列出 `linear_qkv`、`linear_proj`、`linear_fc1`、`linear_fc2` 或通配模式。
- **常见值**：all-linear
- **来源环境变量**：无
- **性能影响**：机制推断：目标模块越多，LoRA 参数、梯度、同步、merge/refit 成本越高；`all-linear` 覆盖广、适配能力强，但开销也高于只选少数层/投影。
- **精度影响**：文档说明：target modules 决定哪些层可被 LoRA 适配；覆盖太窄可能欠拟合，MoE router 默认被排除，若任务需要适配 router 需显式加入。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh:57` actor_rollout_ref.model.target_modules=all-linear

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
