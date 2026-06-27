# actor_rollout_ref.model.lora_adapter_path

- **参数名**：`actor_rollout_ref.model.lora_adapter_path`
- **分类**：配置
- **中文解释**：actor 模型加载已有 LoRA adapter 的路径；FSDP engine 检测到该字段后会用 PEFT 从该路径加载 adapter，并以可训练状态继续训练。
- **常见值**："$LORA_ADAPTER_PATH"
- **来源环境变量**：无
- **性能影响**：机制推断：会增加启动时 adapter 读取和本地复制开销；训练性能主要取决于 LoRA 配置、目标模块和是否只训练 adapter。
- **精度影响**：机制推断：直接决定继续训练的 adapter 初始权重；加载不同 adapter 会改变模型行为和后续收敛轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh:51` actor_rollout_ref.model.lora_adapter_path="$LORA_ADAPTER_PATH"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
