# actor_rollout_ref.actor.mindspeed.mcore_kwargs.seq_length

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.seq_length`
- **分类**：效率
- **中文解释**：文档说明：MindSpeed/Megatron Core 训练侧使用的最大序列长度。示例把它设为 `max_prompt_length + max_response_length`，与 rollout 能处理的 prompt 加 response 总长度对齐。
- **常见值**：$((max_prompt_length + max_response_length))
- **来源环境变量**：无
- **性能影响**：机制推断：序列长度越大，attention 激活、KV/中间张量显存和单步计算时间通常上升；过小会限制可训练样本或导致长度校验失败。
- **精度影响**：机制推断：足够长度可保留完整 prompt/response 信号；过小会截断或拒绝长样本，改变训练数据分布并影响任务准确率。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:130` actor_rollout_ref.actor.mindspeed.mcore_kwargs.seq_length=${max_model_len}
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:135` actor_rollout_ref.actor.mindspeed.mcore_kwargs.seq_length=${max_model_len}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
