# model.use_liger

- **参数名**：`model.use_liger`
- **分类**：效率
- **中文解释**：文档说明：模型侧是否启用 Liger kernel；官方参数表将 `actor_rollout_ref.model.use_liger` 定义为“是否使用 Liger 内核”，SFT 示例通过 `model.use_liger=True` 开启。
- **常见值**：True"
- **来源环境变量**：无
- **性能影响**：机制推断：Liger 通常提供融合/优化 kernel，可减少显存占用并提升支持模型上的训练吞吐；收益取决于模型结构、序列长度和 Liger 版本兼容性。
- **精度影响**：机制推断：不改变训练目标；融合 kernel 的计算顺序和低精度路径可能带来细小数值差异，不支持的模型或多模态路径需先验证。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:47` extra_args+=("model.use_liger=True")

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
