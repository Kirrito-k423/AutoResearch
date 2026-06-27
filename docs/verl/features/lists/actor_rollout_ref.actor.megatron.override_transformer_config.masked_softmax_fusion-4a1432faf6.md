# actor_rollout_ref.actor.megatron.override_transformer_config.masked_softmax_fusion

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.masked_softmax_fusion`
- **分类**：效率
- **中文解释**：机制推断：Megatron Transformer 配置中的 masked softmax 融合开关，用融合实现处理 attention mask 后的 softmax；Verl MCore 配置转换器将 `masked_softmax_fusion` 作为基础 Transformer 配置项默认启用。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：融合 masked softmax 可减少 attention 中 mask、softmax 等小算子的 kernel launch 和中间显存读写，通常提升长序列 attention 吞吐。
- **精度影响**：机制推断：数学语义仍是 masked softmax；融合 kernel 可能改变归约顺序和低精度舍入，通常只造成微小数值差异，兼容性问题会以运行失败或回退表现。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:161` +actor_rollout_ref.actor.megatron.override_transformer_config.masked_softmax_fusion=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
