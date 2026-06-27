# DEVICE

- **参数名**：`DEVICE`
- **分类**：效率
- **中文解释**：文档说明：examples 脚本中的用户侧设备选择开关，通常自动探测 `torch_npu` 后在 `gpu`/`npu` 路径间切换，也可手动覆盖用于特殊平台。
- **常见值**：$(python3 -c 'import torch_npu' 2>/dev/null && echo npu || echo gpu)
- **来源环境变量**：DEVICE
- **性能影响**：机制推断：决定使用 CUDA/GPU 还是 Ascend/NPU 分支，影响可用后端、通信库、compile/offload 开关和设备数默认值，是平台性能差异的入口参数。
- **精度影响**：机制推断：不直接改变算法；不同硬件/算子实现和精度支持可能带来数值差异，错误选择会导致脚本进入不兼容分支。
- **NPU/Ascend 证据**：是
- **CI 看护**：部分
- **示例数**：14
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:9` DEVICE=${DEVICE:-$(python3 -c 'import torch_npu' 2>/dev/null && echo npu || echo gpu)}
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:9` DEVICE=${DEVICE:-$(python3 -c 'import torch_npu' 2>/dev/null && echo npu || echo gpu)}
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:12` DEVICE=${DEVICE:-$(python3 -c 'import torch_npu' 2>/dev/null && echo npu || echo gpu)}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:6` DEVICE=${DEVICE:-$(python3 -c 'import torch_npu' 2>/dev/null && echo npu || echo gpu)}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:9` DEVICE=${DEVICE:-$(python3 -c 'import torch_npu' 2>/dev/null && echo npu || echo gpu)}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
