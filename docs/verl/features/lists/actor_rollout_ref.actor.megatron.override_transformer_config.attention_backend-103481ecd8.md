# actor_rollout_ref.actor.megatron.override_transformer_config.attention_backend

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.attention_backend`
- **分类**：效率
- **中文解释**：文档说明：Megatron Transformer 覆盖配置中的注意力后端选择，官方参数表给出默认后端为 `flash`，示例设为 `auto` 让后端按模型和环境自动选择可用 attention 实现。
- **常见值**：auto
- **来源环境变量**：无
- **性能影响**：机制推断：不同 attention backend 会显著影响注意力 kernel 吞吐、显存占用和支持的序列长度；`auto` 可提升兼容性，但最终性能取决于被选中的 flash/普通实现及硬件。
- **精度影响**：机制推断：目标上应等价于同一 attention 公式，但不同 kernel 的归约顺序、mask 处理和低精度支持会带来小幅数值差异；选择不兼容后端可能直接失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:130` ++actor_rollout_ref.actor.megatron.override_transformer_config.attention_backend=auto

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
