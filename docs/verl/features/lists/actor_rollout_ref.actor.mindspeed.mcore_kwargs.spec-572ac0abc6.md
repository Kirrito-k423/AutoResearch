# actor_rollout_ref.actor.mindspeed.mcore_kwargs.spec

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.spec`
- **分类**：效率
- **中文解释**：机制推断：传给 MindSpeed/Megatron Core 的 layer spec/provider 配置，用来选择具体模型层实现。示例中的 `qwen3_spec, layer_spec` 表示按 Qwen3 的 MindSpeed LLM layer spec 构造训练侧网络。
- **常见值**：'[mindspeed_llm.tasks.models.spec.qwen3_spec, layer_spec]'
- **来源环境变量**：无
- **性能影响**：机制推断：layer spec 决定是否走 MindSpeed/MCore 的 fused attention、norm、SwiGLU、sequence parallel 等实现；匹配硬件的 spec 可提升吞吐，错误 spec 会造成启动或 kernel 兼容问题。
- **精度影响**：机制推断：应与模型架构严格匹配；若 spec 选错，可能改变层结构、归一化/激活实现或权重命名，导致加载失败或训推数值不一致。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:129` actor_rollout_ref.actor.mindspeed.mcore_kwargs.spec='[mindspeed_llm.tasks.models.spec.qwen3_spec, layer_spec]'
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:134` actor_rollout_ref.actor.mindspeed.mcore_kwargs.spec='[mindspeed_llm.tasks.models.spec.qwen3_spec, layer_spec]'

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
