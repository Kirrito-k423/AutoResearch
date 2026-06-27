# ppo_max_token_len_per_gpu

- **参数名**：`ppo_max_token_len_per_gpu`
- **分类**：效率
- **中文解释**：文档说明：示例脚本中的每 GPU PPO 动态 batch token 上限变量，通常传给 actor/ref/rollout 的 `*_max_token_len_per_gpu`，用于按 token 数而不是固定样本数切分 micro batch。
- **常见值**：$(((max_prompt_length + max_response_length) * 2))
- **来源环境变量**：ppo_max_token_len_per_gpu
- **性能影响**：文档说明：在 `use_dynamic_bsz=True` 时，较大的 token 上限可提高单次计算吞吐和 GPU 利用率，但过大容易 OOM；过小会增加 micro batch 次数并降低吞吐。
- **精度影响**：机制推断：只改变动态分批大小，不改变 PPO/GRPO 损失；若过大导致 OOM 或过小导致训练极慢，才会间接影响稳定性和实验可完成性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:68` ppo_max_token_len_per_gpu=${ppo_max_token_len_per_gpu:-$(((max_prompt_length + max_response_length) * 2))}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
