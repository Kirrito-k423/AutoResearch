# engine.use_mbridge

- **参数名**：`engine.use_mbridge`
- **分类**：效率
- **中文解释**：文档说明：SFT/engine 配置中启用 MBridge 权重转换能力，用于 Megatron/MCore 权重与 Verl engine 之间的格式适配。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响模型初始化、权重转换和 checkpoint 兼容；机制推断：对稳定训练 step 吞吐通常不是直接旋钮，但转换失败会阻塞启动。
- **精度影响**：机制推断：正确转换时不改变模型语义；若源 checkpoint、配置或转换路径不匹配，可能加载错误权重并直接影响训练/评测结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:63` engine.use_mbridge=True \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:57` engine.use_mbridge=True
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:59` engine.use_mbridge=True
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:68` engine.use_mbridge=True \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:117` engine.use_mbridge=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
