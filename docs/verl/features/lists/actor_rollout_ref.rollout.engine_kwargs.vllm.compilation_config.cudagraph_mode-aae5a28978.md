# actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_mode

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_mode`
- **分类**：效率
- **中文解释**：文档说明：传给 vLLM `compilation_config` 的 CUDA Graph 捕获模式。示例使用 `FULL_DECODE_ONLY`，表示主要对 decode 阶段启用完整图模式；Verl Ascend 性能指南也把它和 `enforce_eager=False`、capture sizes 一起作为图模式配置。
- **常见值**："FULL_DECODE_ONLY"、FULL_DECODE_ONLY
- **来源环境变量**：无
- **性能影响**：文档说明：图模式通过提前捕获/复用计算图降低 rollout decode 的调度和 kernel launch 开销，通常提升推理吞吐；代价是额外显存占用、捕获耗时和对动态 shape 的兼容约束。
- **精度影响**：机制推断：不改变采样分布或训练目标；但图模式兼容问题导致的回退、失败或 batch 调整会间接影响训练可复现性和稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:117` +actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_mode="FULL_DECODE_ONLY"
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:174` +actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_mode=FULL_DECODE_ONLY

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
