# CLIP_LOW

- **参数名**：`CLIP_LOW`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，通常传给 `actor_rollout_ref.actor.clip_ratio_low`，控制 PPO/DAPO policy ratio 的下裁剪界；CISPO 示例也说明可用特殊大值近似关闭下侧裁剪。
- **常见值**：$CLIP_DEFAULT
- **来源环境变量**：CLIP_LOW
- **性能影响**：机制推断：标量裁剪阈值几乎不增加计算量；它主要改变训练约束，而不是 rollout 或模型前后向吞吐。
- **精度影响**：文档说明：下裁剪界越严格，越限制策略概率下降幅度，可提升稳定性但可能抑制必要更新；过宽会放大训练方差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:23` clip_ratio_low=${CLIP_LOW:-$CLIP_DEFAULT}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
