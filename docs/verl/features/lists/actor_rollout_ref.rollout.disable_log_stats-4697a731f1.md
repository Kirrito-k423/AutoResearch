# actor_rollout_ref.rollout.disable_log_stats

- **参数名**：`actor_rollout_ref.rollout.disable_log_stats`
- **分类**：效率
- **中文解释**：文档说明：控制 rollout 推理后端是否禁用统计日志；官方性能调优和 Prometheus/Grafana 文档建议调优或监控时设为 `False`，以便记录 rollout/vLLM/SGLang 统计。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：设为 `False` 会保留统计与 metrics，便于定位 GPU cache、批处理和 spec decode 状态，但有少量日志/指标开销；设为 `True` 可减少观测开销但会失去调优依据，部分 MTP rollout 统计还要求它为 `False`。
- **精度影响**：机制推断：该参数不改变采样分布、奖励或优化目标；主要影响可观测性，只有在缺少必要统计导致特定功能报错或无法调参时才会间接影响训练结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:124` actor_rollout_ref.rollout.disable_log_stats=False \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
