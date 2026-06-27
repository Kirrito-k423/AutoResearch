# --upgrade

- **参数名**：`--upgrade`
- **分类**：效率
- **中文解释**：文档说明：`pip install --upgrade transformers` 的升级标志；相关示例把它写在依赖准备注释中，用来提示安装较新的 Transformers 以匹配模型支持。
- **常见值**：transformers
- **来源环境变量**：无
- **性能影响**：机制推断：主要影响环境准备时间和依赖版本；升级后的 Transformers 可能带来兼容性或实现性能差异，但它不是训练循环中的实时性能开关。
- **精度影响**：机制推断：通常不直接改变目标函数；依赖版本变化可能改变 tokenizer、模型实现或默认配置，从而影响复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:14` #       pip install --upgrade transformers
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:7` #       pip install --upgrade transformers
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:8` #       pip install --upgrade transformers

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
