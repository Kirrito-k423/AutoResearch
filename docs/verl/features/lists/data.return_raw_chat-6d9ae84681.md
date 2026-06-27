# data.return_raw_chat

- **参数名**：`data.return_raw_chat`
- **分类**：效率
- **中文解释**：文档说明：是否在数据样本中返回未套 chat template 的原始 chat/prompt；Verl 配置文档说明它用于保留原始对话内容，常见于多轮、工具调用或 reward/env 需要原始 chat 的场景。
- **常见值**：$return_raw_chat、True
- **来源环境变量**：return_raw_chat
- **性能影响**：机制推断：通常只增加少量数据加载、序列化和内存占用，不改变模型前后向吞吐主路径。
- **精度影响**：机制推断：本身不改变模型损失；但 reward、agent loop 或工具调用若依赖原始 chat，关闭会改变输入口径并影响评测/训练结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:41` data.return_raw_chat=True
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:136` data.return_raw_chat=True
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:98` data.return_raw_chat=$return_raw_chat
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:120` data.return_raw_chat=True
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:33` "data.return_raw_chat=${return_raw_chat}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
