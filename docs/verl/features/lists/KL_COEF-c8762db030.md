# KL_COEF

- **参数名**：`KL_COEF`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `algorithm.kl_ctrl.kl_coef`，表示 reward 侧 KL penalty 的初始/固定系数，用于把当前策略相对参考模型的偏离惩罚加入 reward。
- **常见值**：0.0
- **来源环境变量**：KL_COEF
- **性能影响**：机制推断：系数本身几乎不影响吞吐；启用 reward 侧 KL 时，主要成本来自参考/旧策略 log-prob 等前向或统计路径。
- **精度影响**：文档说明：系数越大越强约束策略偏离，通常提升稳定性并抑制 reward hacking，但会压缩探索和奖励优化空间；系数越小则相反。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:21` kl_coef=${KL_COEF:-0.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
