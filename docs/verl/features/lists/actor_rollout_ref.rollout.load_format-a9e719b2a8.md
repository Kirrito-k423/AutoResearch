# actor_rollout_ref.rollout.load_format

- **参数名**：`actor_rollout_ref.rollout.load_format`
- **分类**：效率
- **中文解释**：文档说明：选择 rollout 推理引擎加载 actor 权重时使用的格式/加载器；`auto` 由后端自动选择，`safetensors` 明确按 safetensors 权重加载，常用于 vLLM/SGLang 初始化和 LoRA/权重同步场景。
- **常见值**：auto、safetensors
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响 rollout engine 启动、权重加载和显存评估路径；真实权重加载更可靠但可能增加初始化 I/O，自动加载可减少手工适配成本。机制推断：训练 step 吞吐通常不由该参数直接决定。
- **精度影响**：文档说明：`auto`/`safetensors` 若加载同一份权重通常不改变数学计算；若误用 dummy/错误权重格式导致 rollout 权重与 actor 不一致，则生成结果和后续 RL 信号会明显失真。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_from_adapter_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:121` actor_rollout_ref.rollout.load_format=auto
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:108` actor_rollout_ref.rollout.load_format=safetensors
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:103` actor_rollout_ref.rollout.load_format=auto
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:79` actor_rollout_ref.rollout.load_format=safetensors
- `examples/tuning/lora/run_qwen3_8b_fsdp.sh:76` actor_rollout_ref.rollout.load_format=safetensors

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
