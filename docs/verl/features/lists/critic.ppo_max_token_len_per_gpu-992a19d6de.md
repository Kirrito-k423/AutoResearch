# critic.ppo_max_token_len_per_gpu

- **参数名**：`critic.ppo_max_token_len_per_gpu`
- **分类**：效率
- **中文解释**：Critic 在动态 batch 模式下每张 GPU 处理 `update_critic` 前向/反向的最大 token 数，用于替代固定 micro batch size 的手工调参。
- **常见值**：24576、8192
- **来源环境变量**：PPO_MAX_TOKEN_LEN_PER_GPU
- **性能影响**：文档说明：Verl 性能调优文档建议在 `use_dynamic_bsz=True` 时调大此类 token 上限以获得更高吞吐，但过大可能 OOM；critic/reward 的上限通常可设为 actor 的 2 倍左右。
- **精度影响**：机制推断：该参数只限制 critic 计算时的动态分批规模，不改变 value loss 定义；若过小导致吞吐差或过大导致 OOM，才会间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:111` critic.ppo_max_token_len_per_gpu=${PPO_MAX_TOKEN_LEN_PER_GPU}
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:98` critic.ppo_max_token_len_per_gpu=${ppo_max_token_len_per_gpu}
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:85` critic.ppo_max_token_len_per_gpu=8192 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
