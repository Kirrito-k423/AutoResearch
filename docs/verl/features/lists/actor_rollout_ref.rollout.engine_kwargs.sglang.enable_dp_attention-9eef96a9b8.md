# actor_rollout_ref.rollout.engine_kwargs.sglang.enable_dp_attention

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.sglang.enable_dp_attention`
- **分类**：效率
- **中文解释**：传给 SGLang 的 DP attention 开关，启用后 attention 使用数据并行、FFN 使用张量并行；SGLang 官方源码说明主要面向 DeepSeek-V2 和 Qwen 2/3 MoE 等模型。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：SGLang 要求 DP size 与 TP size 匹配，启用后会改变 attention/FFN 并行布局，并可能联动调整 chunked prefill；配置不当会带来通信或兼容性问题。
- **精度影响**：机制推断：并行布局不应改变模型语义；除浮点归约顺序差异或后端兼容性问题外，通常不直接影响精度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:176` +actor_rollout_ref.rollout.engine_kwargs.sglang.enable_dp_attention=False
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:177` +actor_rollout_ref.rollout.engine_kwargs.sglang.enable_dp_attention=False
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:188` +actor_rollout_ref.rollout.engine_kwargs.sglang.enable_dp_attention=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
