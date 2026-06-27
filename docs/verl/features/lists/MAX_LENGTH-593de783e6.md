# MAX_LENGTH

- **参数名**：`MAX_LENGTH`
- **分类**：效率
- **中文解释**：机制推断：SFT 示例中的最大序列长度，写入 `data.max_length` 和 `data.max_token_len_per_gpu`，用于限制单条样本/每 GPU 可处理 token 上限。
- **常见值**：2048
- **来源环境变量**：MAX_LENGTH
- **性能影响**：文档说明：长序列训练需要降低 micro batch 或 max token len 来避免 OOM；增大 `MAX_LENGTH` 会提高激活/KV/注意力计算与显存需求。
- **精度影响**：机制推断：更长上限能保留更多上下文和标签 token；过短会触发截断/报错或丢失训练信息，过长则可能通过更小 batch 间接影响优化稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:69` MAX_LENGTH=${MAX_LENGTH:-2048}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
