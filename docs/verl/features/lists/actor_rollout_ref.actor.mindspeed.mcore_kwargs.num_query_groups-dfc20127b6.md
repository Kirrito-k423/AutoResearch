# actor_rollout_ref.actor.mindspeed.mcore_kwargs.num_query_groups

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.num_query_groups`
- **分类**：效率
- **中文解释**：机制推断：传给 MindSpeed/Megatron Core 的 GQA/MQA 参数，表示 attention 中 query heads 共享的 KV query group 数量。该值应与模型结构或转换后的 Megatron 配置一致。
- **常见值**：4、8
- **来源环境变量**：无
- **性能影响**：机制推断：决定注意力 KV 头分组形状，影响 KV cache、attention kernel 形状和张量并行切分；较少 KV group 通常降低内存和通信，但必须匹配模型。
- **精度影响**：机制推断：这是模型结构参数；与预训练权重一致时不额外影响精度，若填错会改变 attention 拓扑、导致权重无法加载或生成质量异常。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:132` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.num_query_groups=8
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:137` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.num_query_groups=4

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
