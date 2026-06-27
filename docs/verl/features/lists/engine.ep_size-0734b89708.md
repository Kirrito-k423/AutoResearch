# engine.ep_size

- **参数名**：`engine.ep_size`
- **分类**：效率
- **中文解释**：设置 AutoModel/MoE 场景下的专家并行（expert parallel）大小，把不同 MoE experts 分布到多个 rank 上；examples 中小模型为 1，Qwen3-30B-A3B AutoModel 示例为 8。
- **常见值**：1、8
- **来源环境变量**：无
- **性能影响**：文档说明：EP 并行可降低单 rank 专家参数/计算压力、扩展 MoE 模型容量，但会引入 token dispatch、all-to-all 通信和负载均衡开销。
- **精度影响**：机制推断：EP 切分不应改变等价模型的目标函数；但专家负载不均、并行通信或可训练模型规模变化会间接影响稳定性和效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:36` engine.ep_size=1 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:39` engine.ep_size=8 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
