# return_raw_chat

- **参数名**：`return_raw_chat`
- **分类**：效率
- **中文解释**：文档说明：示例环境变量，最终写入 `data.return_raw_chat`；控制数据集样本中是否返回原始 chat/prompt 内容，供 reward、agent loop 或日志链路使用。
- **常见值**：True
- **来源环境变量**：return_raw_chat
- **性能影响**：机制推断：开启后每个样本携带更多原始文本/结构化消息，可能略增数据传输、内存和日志体积；通常不是主要性能瓶颈。
- **精度影响**：机制推断：若 reward function、tool/agent loop 或评测逻辑需要原始 chat，上游关闭会改变可用输入并影响结果；普通纯 prompt/token 训练中通常不直接改变损失。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:16` return_raw_chat=${return_raw_chat:-True}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
