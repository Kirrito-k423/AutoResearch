# MODEL_NAME

- **参数名**：`MODEL_NAME`
- **分类**：配置
- **中文解释**：Nemotron SFT 示例中的模型名称变量，默认拼成 `MODEL_PATH=nvidia/${MODEL_NAME}`，同时参与实验名生成。
- **常见值**：NVIDIA-Nemotron-3-Nano-30B-A3B-BF16
- **来源环境变量**：MODEL_NAME
- **性能影响**：机制推断：变量本身无开销；选择的模型大小、MoE 结构和本地/远程加载位置会决定显存、吞吐和下载启动时间。
- **精度影响**：机制推断：它决定实际加载的基座模型；换模型会直接改变初始能力、tokenizer/配置兼容性和最终 SFT 结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:23` MODEL_NAME=${MODEL_NAME:-NVIDIA-Nemotron-3-Nano-30B-A3B-BF16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
