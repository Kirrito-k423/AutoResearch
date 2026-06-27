# USE_LIGER

- **参数名**：`USE_LIGER`
- **分类**：效率
- **中文解释**：SFT 示例中的开关；当 `USE_LIGER=1` 时追加 `model.use_liger=True`，启用 LigerKernel 对模型内部 RMSNorm、SwiGLU、RoPE 等 Triton fused kernels 的优化。
- **常见值**：0
- **来源环境变量**：USE_LIGER
- **性能影响**：文档说明：Verl perf tuning 说明 LigerKernel 可提升 SFT/RL 训练吞吐，且与 `use_fused_kernels` 兼容；需要安装 `liger-kernel`，不支持或未安装时会影响可用性。
- **精度影响**：机制推断：Liger 通常是等价 fused kernel 优化，不改变训练目标；但 fused kernel 的低层数值路径可能带来极小差异，兼容性问题会表现为运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:33` USE_LIGER=${USE_LIGER:-0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
