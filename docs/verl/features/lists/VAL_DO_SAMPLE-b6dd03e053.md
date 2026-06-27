# VAL_DO_SAMPLE

- **参数名**：`VAL_DO_SAMPLE`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.val_kwargs.do_sample`，控制验证阶段是否启用采样；官方参数表默认 false，最佳实践给出 `do_sample=True` 作为小测试集验证起点之一。
- **常见值**：True
- **来源环境变量**：VAL_DO_SAMPLE
- **性能影响**：机制推断：采样本身开销小；若与验证 `n` 增大或更长输出结合，会增加验证生成成本。
- **精度影响**：文档说明：它改变验证口径：False 更接近贪心、方差低；True 保留随机性，适合小测试集结合多次采样估计能力，但评测波动更大。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:69` val_do_sample=${VAL_DO_SAMPLE:-True}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
