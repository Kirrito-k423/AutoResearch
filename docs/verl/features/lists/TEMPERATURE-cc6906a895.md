# TEMPERATURE

- **参数名**：`TEMPERATURE`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，既可用于训练 rollout 的 `actor_rollout_ref.rollout.temperature`，也常同步传给验证 `val_kwargs.temperature`，用于调节 token 分布随机性。
- **常见值**：1.0
- **来源环境变量**：TEMPERATURE
- **性能影响**：机制推断：温度缩放本身开销很小；但改变输出长度、EOS 分布和验证/训练采样路径，可能间接影响耗时。
- **精度影响**：文档说明：temperature 直接改变采样分布；较高值增加探索和评测方差，较低值更确定但可能降低多样性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:27` temperature=${TEMPERATURE:-1.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
