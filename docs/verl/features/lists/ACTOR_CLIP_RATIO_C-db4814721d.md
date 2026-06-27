# ACTOR_CLIP_RATIO_C

- **参数名**：`ACTOR_CLIP_RATIO_C`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.actor.clip_ratio_c`；它是 Dual-clip PPO 的额外裁剪常数，官方 PPO 文档说明在负优势样本上限制 policy ratio 相关项，默认约 3.0，examples 常设 10.0。
- **常见值**：10.0
- **来源环境变量**：ACTOR_CLIP_RATIO_C
- **性能影响**：机制推断：只是 actor loss 中的标量阈值/条件裁剪计算，相对模型前后向开销可忽略。
- **精度影响**：文档说明：直接改变 PPO surrogate objective 的负优势样本约束；值越小保护越强、更新更保守，值越大越接近弱化 dual-clip 限制。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:37` actor_clip_ratio_c=${ACTOR_CLIP_RATIO_C:-10.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
