# model.trust_remote_code

- **参数名**：`model.trust_remote_code`
- **分类**：效率
- **中文解释**：文档说明：控制 Hugging Face 模型/配置/分词器加载时是否信任远端仓库自定义代码；对 Qwen、MiniCPM、Moonlight 等带自定义建模文件的模型可能是必要开关。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：不直接决定训练吞吐；自定义模型代码可能影响初始化耗时、算子实现和兼容性，也带来代码执行安全成本。
- **精度影响**：机制推断：若模型依赖自定义 architecture，关闭可能加载失败或无法复现正确前向；开启后只要代码与权重匹配，参数本身不应改变数学目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:36` model.trust_remote_code=True
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:87` model.trust_remote_code=True \
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:91` model.trust_remote_code=True \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:147` model.trust_remote_code=True \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:32` model.trust_remote_code=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
