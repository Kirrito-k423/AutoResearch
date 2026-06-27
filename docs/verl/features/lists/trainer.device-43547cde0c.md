# trainer.device

- **参数名**：`trainer.device`
- **分类**：效率
- **中文解释**：文档说明：指定 trainer 使用的设备类型，例如 `cuda` 或 `npu`；Ascend examples 显式设置为 `npu`，用于让 Verl 选择 torch_npu/NPU 后端与相关设备可见性逻辑。
- **常见值**：'npu'、npu
- **来源环境变量**：无
- **性能影响**：机制推断：是硬件后端选择，影响可用 kernel、通信库、显存容量和整体吞吐；`npu` 需要配套 Ascend/CANN/torch_npu/SGLang Ascend 后端。
- **精度影响**：机制推断：设备选择本身不改变算法目标；不同硬件后端的 kernel、混合精度和通信实现可能产生数值微差，未完成精度对齐时需单独验证。
- **NPU/Ascend 证据**：是
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:197` trainer.device='npu'
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:147` trainer.device=npu
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:198` trainer.device='npu'
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:189` trainer.device='npu'
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:209` trainer.device='npu'

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
