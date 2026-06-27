# ROLLOUT_MAX_MODEL_LEN

- **参数名**：`ROLLOUT_MAX_MODEL_LEN`
- **分类**：效率
- **中文解释**：控制 `actor_rollout_ref.rollout.max_model_len`，即 rollout 推理后端可接收的最大序列长度；示例中为 Qwen3-30B-A3B 设置为 10240，用来覆盖 prompt 与 response 的总长度预算。
- **常见值**：10240
- **来源环境变量**：ROLLOUT_MAX_MODEL_LEN
- **性能影响**：机制推断：值越大，KV cache、调度预留和 prefill/decode 时间通常上升；值过小会限制可进入 rollout 的长样本，可能导致后端报错或需要降低并发。
- **精度影响**：机制推断：足够覆盖 `max_prompt_length + max_response_length` 时通常不直接改变精度；设得过小会截断或拒绝长样本，改变训练/评测数据分布。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:59` rollout_max_model_len=${ROLLOUT_MAX_MODEL_LEN:-10240}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
