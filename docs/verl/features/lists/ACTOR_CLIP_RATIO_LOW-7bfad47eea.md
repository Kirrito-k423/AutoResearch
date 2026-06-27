# ACTOR_CLIP_RATIO_LOW

- **参数名**：`ACTOR_CLIP_RATIO_LOW`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.actor.clip_ratio_low`，表示 PPO/DAPO importance sampling ratio 的下裁剪界；DAPO 文档用它表示目标里的下界 epsilon。
- **常见值**：0.2
- **来源环境变量**：ACTOR_CLIP_RATIO_LOW
- **性能影响**：机制推断：仅改变 loss 中的标量裁剪阈值，计算开销可忽略；主要影响训练动态而非吞吐。
- **精度影响**：文档说明：下界越严格，越限制策略概率下降幅度，可提升稳定性但可能抑制必要更新；过宽则可能带来更大方差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:35` actor_clip_ratio_low=${ACTOR_CLIP_RATIO_LOW:-0.2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
