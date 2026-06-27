# LORA_ADAPTER_PATH

- **参数名**：`LORA_ADAPTER_PATH`
- **分类**：配置
- **中文解释**：LoRA adapter 的路径环境变量；LoRA resume 示例要求必须设置，并把它传给 `actor_rollout_ref.model.lora_adapter_path` 以加载已有 adapter 继续训练。
- **常见值**：?must set LORA_ADAPTER_PATH
- **来源环境变量**：LORA_ADAPTER_PATH
- **性能影响**：机制推断：启动时需要读取 adapter 权重并可能复制到本地；训练阶段开销取决于 LoRA 配置本身，路径变量主要影响加载时间与 I/O 可靠性。
- **精度影响**：机制推断：会改变继续训练的初始 adapter 权重；路径指向不同 adapter 等同于从不同微调状态继续，直接影响收敛和最终效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh:9` LORA_ADAPTER_PATH=${LORA_ADAPTER_PATH:?must set LORA_ADAPTER_PATH}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
