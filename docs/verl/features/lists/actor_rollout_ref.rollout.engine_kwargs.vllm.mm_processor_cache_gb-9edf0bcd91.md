# actor_rollout_ref.rollout.engine_kwargs.vllm.mm_processor_cache_gb

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.vllm.mm_processor_cache_gb`
- **分类**：效率
- **中文解释**：传给 vLLM 的多模态 processor cache 容量（GiB），用于缓存图片/视频等多模态预处理结果；示例中设为 `0` 表示禁用该缓存。
- **常见值**：0
- **来源环境变量**：无
- **性能影响**：文档说明：vLLM 官方源码默认该缓存为 4 GiB，并会按 API/engine 进程和 DP 副本复制；增大可减少重复预处理，设为 0 可节省内存但可能增加预处理耗时。
- **精度影响**：机制推断：缓存只保存确定性的多模态预处理结果，不改变模型权重或采样策略；正常情况下不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:124` +actor_rollout_ref.rollout.engine_kwargs.vllm.mm_processor_cache_gb=0
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh:130` +actor_rollout_ref.rollout.engine_kwargs.vllm.mm_processor_cache_gb=0
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:91` +actor_rollout_ref.rollout.engine_kwargs.vllm.mm_processor_cache_gb=0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
