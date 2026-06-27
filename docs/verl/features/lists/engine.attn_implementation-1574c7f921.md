# engine.attn_implementation

- **参数名**：`engine.attn_implementation`
- **分类**：效率
- **中文解释**：文档说明：Automodel/SFT engine 使用的 attention backend；engine 配置支持 `sdpa`、`flash_attention_2`、`eager`、`te`，示例设置为 Transformer Engine 的 `te`。
- **常见值**：te
- **来源环境变量**：无
- **性能影响**：文档说明：不同 attention 实现有不同性能/显存特征，FlashAttention/TE 通常更高吞吐更省显存，`eager` 更适合调试和兼容性排错。
- **精度影响**：机制推断：不同 attention backend 目标等价，但 kernel 融合、低精度累加和 mask 实现可能带来微小数值差异；不兼容实现会报错或需要回退。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:48` engine.attn_implementation=te \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
