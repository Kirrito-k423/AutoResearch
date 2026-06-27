# ENTRYPOINT

- **参数名**：`ENTRYPOINT`
- **分类**：效率
- **中文解释**：文档说明：`torchrun` 最终执行的 Python 入口，示例默认 `-m verl.trainer.sft_trainer`，用于启动 Verl SFT 多进程训练。
- **常见值**："-m verl.trainer.sft_trainer"
- **来源环境变量**：ENTRYPOINT
- **性能影响**：机制推断：入口本身不是性能旋钮；更换入口会切换训练器实现、数据流和分布式初始化路径，从而间接改变启动和训练开销。
- **精度影响**：机制推断：默认 SFT 入口按 SFT 目标训练；若改成其它 trainer 或脚本，会改变训练目标、数据处理或损失计算。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:8` ENTRYPOINT=${ENTRYPOINT:-"-m verl.trainer.sft_trainer"}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:13` ENTRYPOINT=${ENTRYPOINT:-"-m verl.trainer.sft_trainer"}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:26` ENTRYPOINT=${ENTRYPOINT:-"-m verl.trainer.sft_trainer"}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。
