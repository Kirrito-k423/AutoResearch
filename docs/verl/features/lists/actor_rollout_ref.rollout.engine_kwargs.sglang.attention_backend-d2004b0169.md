# actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend`
- **分类**：效率
- **中文解释**：文档说明：传给 SGLang rollout engine 的 attention backend 选择；NPU/Ascend 文档要求设置为 `ascend` 以调用昇腾优化内核，GPU examples 中也会出现 `flashinfer`、`triton` 等后端。
- **常见值**："ascend"、ascend、flashinfer、triton
- **来源环境变量**：无
- **性能影响**：文档说明：直接决定 rollout 注意力 kernel/后端，影响生成吞吐、显存和平台兼容性；错误后端可能无法启动，合适后端可利用硬件优化。
- **精度影响**：机制推断：不同 attention backend 理论上实现同一注意力语义，但可能因 kernel 精度、mask 处理和平台实现差异产生微小数值差异；后端不兼容时会直接报错或生成异常。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:105` actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend=triton
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:86` EXTRA+=(+actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend=flashinfer)
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:122` +actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend=ascend
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:161` +actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend="ascend"
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:161` +actor_rollout_ref.rollout.engine_kwargs.sglang.attention_backend="ascend"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
