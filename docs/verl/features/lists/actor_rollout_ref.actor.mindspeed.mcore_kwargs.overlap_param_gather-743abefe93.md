# actor_rollout_ref.actor.mindspeed.mcore_kwargs.overlap_param_gather

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.overlap_param_gather`
- **分类**：效率
- **中文解释**：机制推断：MindSpeed/Megatron Core 的参数聚合重叠开关，用于在参数分片/分布式优化器场景中提前 gather 下一段计算需要的模型参数。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：可把参数 all-gather 通信与前向/反向计算重叠，减少等待时间；可能增加参数预取缓冲和峰值显存，对拓扑与 bucket 配置敏感。
- **精度影响**：机制推断：正确实现时不改变模型计算；若 gather 时序或分片配置错误，会导致使用错误参数片并影响 loss、logprob 和训练稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:137` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.overlap_param_gather=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
