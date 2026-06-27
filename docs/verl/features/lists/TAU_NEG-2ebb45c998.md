# TAU_NEG

- **参数名**：`TAU_NEG`
- **分类**：效率
- **中文解释**：源码说明：SAPO 策略损失中负优势 token 使用的 tau 参数；当 advantage 小于等于 0 时，源码用 `tau_neg` 进入门控函数来调节 importance ratio 的更新权重。
- **常见值**：1.05
- **来源环境变量**：TAU_NEG
- **性能影响**：机制推断：只是策略损失中的标量门控参数，额外计算开销可忽略；不会直接改变吞吐或显存。
- **精度影响**：源码说明：直接改变负优势样本的策略梯度门控曲线；值过大或过小都会改变对坏动作概率的压制力度，影响 SAPO 稳定性和最终效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh:22` tau_neg=${TAU_NEG:-1.05}
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh:14` tau_neg=${TAU_NEG:-1.05}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
