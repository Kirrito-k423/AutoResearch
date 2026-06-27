# OVERLONG_PENALTY_FACTOR

- **参数名**：`OVERLONG_PENALTY_FACTOR`
- **分类**：效率
- **中文解释**：文档说明：DAPO overlong buffer 的最大惩罚强度；回复长度越接近最大响应长度，线性负奖励越接近 `-penalty_factor`。
- **常见值**：1.0
- **来源环境变量**：OVERLONG_PENALTY_FACTOR
- **性能影响**：机制推断：只改变奖励标量幅度，直接计算成本基本不变；较大惩罚可能间接减少模型生成冗长答案的倾向。
- **精度影响**：文档说明：该值直接控制超长回复负奖励幅度；值越大越强烈抑制长回复，可能改善长度控制，也可能伤害依赖长链路推理的任务表现。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:51` overlong_penalty_factor=${OVERLONG_PENALTY_FACTOR:-1.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
