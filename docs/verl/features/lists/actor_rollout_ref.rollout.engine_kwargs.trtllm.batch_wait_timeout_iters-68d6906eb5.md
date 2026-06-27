# actor_rollout_ref.rollout.engine_kwargs.trtllm.batch_wait_timeout_iters

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.trtllm.batch_wait_timeout_iters`
- **分类**：效率
- **中文解释**：机制推断：传给 TensorRT-LLM rollout 后端的批等待超时迭代数，限制动态 batching 为凑批最多等待多少调度轮次；示例在 trtllm 后端下设置为 32。
- **常见值**：32
- **来源环境变量**：无
- **性能影响**：机制推断：更大的等待轮次可能形成更大的有效 batch、提升吞吐，但会提高排队延迟和尾部等待；更小的值降低等待延迟，但可能让 GPU 批量不足。
- **精度影响**：机制推断：该参数只改变请求调度时机，不直接改变模型概率或采样；若等待策略造成 rollout 产样节奏显著变化，才可能通过异步队列或超时失败间接影响训练。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:232` +actor_rollout_ref.rollout.engine_kwargs.trtllm.batch_wait_timeout_iters=32

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
