# engine.use_torch_compile

- **参数名**：`engine.use_torch_compile`
- **分类**：效率
- **中文解释**：控制 engine/FSDP/AutoModel 路径是否使用 `torch.compile` 或相关 JIT 编译优化；Verl FAQ 提到遇到 Triton 编译错误时可关闭该类 `use_torch_compile` 开关。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：开启后可能通过图编译和融合内核提升吞吐，但会增加首次编译时间、缓存/显存压力和编译失败风险；关闭更稳但可能损失部分速度。
- **精度影响**：机制推断：编译本身不改变目标函数；不同融合内核和低精度路径可能导致极小数值差异，通常不是主要精度旋钮。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:37` engine.use_torch_compile=False \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:49` engine.use_torch_compile=False \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
