# global_profiler.tool

- **参数名**：`global_profiler.tool`
- **分类**：配置
- **中文解释**：控制 profiling 采集范围和开销，用于定位耗时/显存问题，通常不直接提升精度。
- **常见值**：npu、torch_memory
- **来源环境变量**：无
- **性能影响**：机制推断：开启 profiling 会增加采集和落盘开销。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`
- `examples/profile/run_qwen3_8b_npu_profile_discrete.sh`
- `examples/profile/run_qwen3_8b_npu_profile_e2e.sh`

## 证据片段

- `examples/profile/run_qwen3_8b_npu_profile_e2e.sh:113` global_profiler.tool=npu
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh:105` global_profiler.tool=torch_memory
- `examples/profile/run_qwen3_8b_npu_profile_discrete.sh:116` global_profiler.tool=npu
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:209` global_profiler.tool=npu
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:210` global_profiler.tool=npu

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
