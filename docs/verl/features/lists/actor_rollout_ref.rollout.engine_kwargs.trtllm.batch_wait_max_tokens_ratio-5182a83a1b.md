# actor_rollout_ref.rollout.engine_kwargs.trtllm.batch_wait_max_tokens_ratio

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.trtllm.batch_wait_max_tokens_ratio`
- **分类**：效率
- **中文解释**：机制推断：传给 TensorRT-LLM rollout 后端的批等待参数，表示动态调度时为了凑批可等待的 token 容量比例；示例在 trtllm 后端下设置为 0.5。
- **常见值**：0.5
- **来源环境变量**：无
- **性能影响**：机制推断：值较高通常允许等待更满的 token batch，提高 GPU 利用率和吞吐，但会增加请求排队/首 token 延迟；值较低更偏低延迟，可能牺牲批处理效率。
- **精度影响**：机制推断：只影响推理调度等待策略，不直接改变 logits、采样参数或训练目标；极端等待导致超时、吞吐瓶颈或 rollout 超长时，才可能通过样本生产节奏间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:233` +actor_rollout_ref.rollout.engine_kwargs.trtllm.batch_wait_max_tokens_ratio=0.5

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
