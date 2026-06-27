# algorithm.lam

- **参数名**：`algorithm.lam`
- **分类**：算法
- **中文解释**：GAE（Generalized Advantage Estimation）的 lambda 参数；PPO README 明确说明它用于在 GAE 估计器的偏差与方差之间做权衡，Ascend 参数表也标注为 GAE lambda。
- **常见值**：$gae_lam
- **来源环境变量**：无
- **性能影响**：机制推断：`lam` 只改变 advantage 计算公式，额外计算量基本不变；性能影响主要来自训练是否更快稳定收敛。
- **精度影响**：文档说明：`lam` 直接控制 GAE 的 bias/variance 取舍；接近 1 方差更高但偏差更低，较小值更平滑但可能引入更多偏差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:133` algorithm.lam=$gae_lam
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:128` algorithm.lam=$gae_lam

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
