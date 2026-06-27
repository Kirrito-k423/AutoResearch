# actor_rollout_ref.rollout.engine_kwargs.vllm.max_model_len

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.vllm.max_model_len`
- **分类**：效率
- **中文解释**：文档说明：透传给 vLLM engine 的最大模型序列长度，约束单条 rollout 请求可处理的 prompt+response 总长度。Verl rollout 配置中 `max_model_len=null` 表示自动推断，Ascend 文档建议设为训练时 `max_prompt_length + max_response_length`。
- **常见值**：$max_model_len"、15768
- **来源环境变量**：无
- **性能影响**：文档说明：`max_model_len` 越大，KV cache 预留、可调度 token 上限和图捕获/批处理内存压力越高；过小会限制长样本，过大可能降低并发或触发 OOM。
- **精度影响**：机制推断：足够长度可保留完整上下文和答案空间；过小会截断、拒绝或提前结束长样本，改变 rollout 奖励和训练数据分布。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:127` +actor_rollout_ref.rollout.engine_kwargs.vllm.max_model_len=$max_model_len"
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:123` +actor_rollout_ref.rollout.engine_kwargs.vllm.max_model_len=15768

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
