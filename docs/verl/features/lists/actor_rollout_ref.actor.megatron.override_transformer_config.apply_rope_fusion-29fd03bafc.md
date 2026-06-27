# actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion`
- **分类**：效率
- **中文解释**：机制推断：向 Megatron Transformer 配置注入 RoPE 融合开关，控制 rotary positional embedding 是否走融合 kernel；Verl examples 对不同大模型显式打开或关闭以适配后端。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：机制推断：融合 RoPE 可减少 kernel 启动和中间张量开销，提升长序列 attention 前处理效率；若模型/后端不兼容，关闭更稳。
- **精度影响**：机制推断：语义上应等价于未融合 RoPE，但融合 kernel 和低精度实现可能产生微小数值差异；兼容性问题比精度收益更关键。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:90` +actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion=True
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:112` +actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion=False
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:115` +actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:160` +actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion=True
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:102` +actor_rollout_ref.actor.megatron.override_transformer_config.apply_rope_fusion=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
