# PAD_MODE

- **参数名**：`PAD_MODE`
- **分类**：效率
- **中文解释**：文档说明：SFT 数据 padding 模式；`no_padding` 会让 collator 返回变长样本/嵌套张量，当前 FSDP、Megatron、AutoModel 等训练路径多处断言只支持 no_padding。
- **常见值**：no_padding
- **来源环境变量**：PAD_MODE
- **性能影响**：文档说明：no_padding/remove padding 路径减少无效 padding token 的计算，能明显提升模型运行效率；不支持的 pad mode 会直接报错。
- **精度影响**：机制推断：正确实现时不改变有效 token 和 loss mask；错误 padding/truncation 或使用不兼容模式可能改变训练样本或导致失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:29` PAD_MODE=${PAD_MODE:-no_padding}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:33` PAD_MODE=${PAD_MODE:-no_padding}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:10` PAD_MODE=${PAD_MODE:-no_padding}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
