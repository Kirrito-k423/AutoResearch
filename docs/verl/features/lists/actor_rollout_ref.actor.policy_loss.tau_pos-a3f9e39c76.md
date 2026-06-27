# actor_rollout_ref.actor.policy_loss.tau_pos

- **参数名**：`actor_rollout_ref.actor.policy_loss.tau_pos`
- **分类**：算法
- **中文解释**：SAPO policy loss 的正优势 token 温度参数；SAPO README 说明该算法用 tau 参数化的平滑 surrogate objective，源码中优势大于 0 时使用 `tau_pos`。
- **常见值**：1.0
- **来源环境变量**：TAU_POS
- **性能影响**：机制推断：`tau_pos` 只改变 SAPO loss 中门控函数的标量计算，单步性能影响很小。
- **精度影响**：文档说明：它直接控制正优势样本的平滑奖励形状；调大/调小会改变对优质动作概率的提升强度，影响策略更新稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh:74` +actor_rollout_ref.actor.policy_loss.tau_pos=${tau_pos}
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh:61` +actor_rollout_ref.actor.policy_loss.tau_pos=${tau_pos}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
