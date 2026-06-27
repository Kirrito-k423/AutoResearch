# actor_rollout_ref.rollout.val_kwargs.do_sample

- **参数名**：`actor_rollout_ref.rollout.val_kwargs.do_sample`
- **分类**：算法
- **中文解释**：文档说明：控制验证阶段是否采样；官方参数表默认 `false`，最佳实践给出验证起点可设 `do_sample=True` 并配合 temperature/top_p/top_k/n。
- **常见值**：True
- **来源环境变量**：VAL_DO_SAMPLE
- **性能影响**：机制推断：采样本身开销小；若与验证 `n` 增大或更长输出结合，会增加验证生成成本。
- **精度影响**：文档说明：它改变验证口径：`False` 更接近贪心、方差低；`True` 保留随机性，适合小测试集结合多次采样估计能力，但评测波动更大。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:118` actor_rollout_ref.rollout.val_kwargs.do_sample=True \
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:132` actor_rollout_ref.rollout.val_kwargs.do_sample=True
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:143` actor_rollout_ref.rollout.val_kwargs.do_sample=True
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:167` actor_rollout_ref.rollout.val_kwargs.do_sample=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:188` actor_rollout_ref.rollout.val_kwargs.do_sample=${val_do_sample}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
