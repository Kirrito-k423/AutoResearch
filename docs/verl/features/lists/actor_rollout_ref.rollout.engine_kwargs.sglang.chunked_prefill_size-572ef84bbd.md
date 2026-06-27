# actor_rollout_ref.rollout.engine_kwargs.sglang.chunked_prefill_size

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.sglang.chunked_prefill_size`
- **分类**：效率
- **中文解释**：传给 SGLang 后端的 chunked prefill 分块大小，表示预填充阶段每个 chunk 的最大 token 数；`-1` 表示关闭 chunked prefill。
- **常见值**：-1
- **来源环境变量**：无
- **性能影响**：文档说明：SGLang server args 说明该值控制 chunked prefill 的 token 上限，激活显存与该值相关；合适的分块可改善长 prompt 调度，`-1` 会让请求保持单次 prefill。
- **精度影响**：机制推断：仅改变 prefill 调度与内存形态，不改变生成分布；正常情况下不直接影响精度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:178` +actor_rollout_ref.rollout.engine_kwargs.sglang.chunked_prefill_size=-1
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:179` +actor_rollout_ref.rollout.engine_kwargs.sglang.chunked_prefill_size=-1
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:190` +actor_rollout_ref.rollout.engine_kwargs.sglang.chunked_prefill_size=-1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
