# actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_capture_sizes

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_capture_sizes`
- **分类**：效率
- **中文解释**：文档说明：传给 vLLM `compilation_config` 的 CUDA Graph 捕获规模列表，用于指定 rollout 推理要为哪些 batch/capture sizes 预捕获执行图。Verl perf 文档说明设置该列表后 vLLM 会尝试为不同 batch size 捕获模型执行图。
- **常见值**："[1, 8, 16, 32, 40, 48, 64, 96, 128, 256]"、[8,16,32,64,128]
- **来源环境变量**：无
- **性能影响**：文档说明：CUDA Graph 可减少推理阶段 kernel launch 开销；覆盖更多/更大的 capture size 通常提高命中率，但会增加图捕获显存和编译/启动成本，过大还可能触发 OOM 或图捕获崩溃。
- **精度影响**：机制推断：图捕获不改变采样参数或模型权重，正常情况下不直接影响精度；但 OOM、回退 eager 或 batch 规模被迫调小会间接影响训练吞吐和稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:90` +actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_capture_sizes="[1, 8, 16, 32, 40, 48, 64, 96, 128, 256]"
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:173` +actor_rollout_ref.rollout.engine_kwargs.vllm.compilation_config.cudagraph_capture_sizes=[8,16,32,64,128]

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
