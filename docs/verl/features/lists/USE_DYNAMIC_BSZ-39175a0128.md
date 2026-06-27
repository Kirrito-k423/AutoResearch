# USE_DYNAMIC_BSZ

- **参数名**：`USE_DYNAMIC_BSZ`
- **分类**：效率
- **中文解释**：控制示例中的 `use_dynamic_bsz`，最终传给 actor 的 `actor_rollout_ref.actor.use_dynamic_bsz`，使训练前向/反向按 token 数动态组 batch，而不是固定样本数。
- **常见值**：True
- **来源环境变量**：USE_DYNAMIC_BSZ
- **性能影响**：文档说明：Verl perf tuning 说明 `use_dynamic_bsz=True` 可显著提升训练效率并降低显存占用；启用后重点调 `ppo_max_token_len_per_gpu`，不再主要调 micro batch。
- **精度影响**：机制推断：动态 batch 不改变目标函数；但 token 上限过低会导致切分过细或无法覆盖长序列，间接影响训练稳定性、吞吐与可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:48` use_dynamic_bsz=${USE_DYNAMIC_BSZ:-True}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
