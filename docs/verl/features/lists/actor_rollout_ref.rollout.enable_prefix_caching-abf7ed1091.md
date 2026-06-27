# actor_rollout_ref.rollout.enable_prefix_caching

- **参数名**：`actor_rollout_ref.rollout.enable_prefix_caching`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理后端的前缀缓存开关；Ascend/Verl 文档将其解释为自动缓存共享前缀、复用 KV Cache，以减少重复 prefill 计算。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：当 prompts 共享系统提示、工具前缀或多轮上下文前缀时，可减少重复 prefill 计算；代价是额外 cache 管理和显存占用。
- **精度影响**：机制推断：正确复用同一前缀 KV 时不改变生成分布；若后端缓存失效或前缀识别不匹配，可能造成运行错误而非算法性精度变化。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:119` actor_rollout_ref.rollout.enable_prefix_caching=False
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:118` actor_rollout_ref.rollout.enable_prefix_caching=False \
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:83` actor_rollout_ref.rollout.enable_prefix_caching=True
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:119` actor_rollout_ref.rollout.enable_prefix_caching=False
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:126` actor_rollout_ref.rollout.enable_prefix_caching=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
