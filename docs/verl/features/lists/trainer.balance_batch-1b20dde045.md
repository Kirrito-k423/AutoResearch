# trainer.balance_batch

- **参数名**：`trainer.balance_batch`
- **分类**：效率
- **中文解释**：控制 trainer 是否对 batch 做负载均衡分配，以减少不同 rank 之间因样本长度或分组导致的工作量不均。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：PrefixGrouper README 写明 `balance_batch=True` 可获得更好的 load distribution，并要求 `batch_size % (world_size * rollout.n) == 0`；开启后可减少慢 rank 拖尾，但需满足整除约束。
- **精度影响**：机制推断：负载均衡不改变样本内容或 loss 定义；若分组约束处理不当导致样本排列/uid 分布变化，才可能间接影响训练统计。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：48
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:122` trainer.balance_batch=True
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:89` trainer.balance_batch=True
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:95` trainer.balance_batch=True
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:132` trainer.balance_batch=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:117` trainer.balance_batch=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
