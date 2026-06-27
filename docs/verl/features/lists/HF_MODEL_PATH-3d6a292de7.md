# HF_MODEL_PATH

- **参数名**：`HF_MODEL_PATH`
- **分类**：配置
- **中文解释**：指定模型权重或模型 ID，是模型规模、结构、显存占用和任务能力的来源。
- **常见值**："${RAY_DATA_HOME、"Qwen/Qwen3.5-122B-A10B"、"Qwen3.5-35B-A3B"、Qwen/Qwen2.5-Math-7B、moonshotai/Moonlight-16B-A3B
- **来源环境变量**：HF_MODEL_PATH
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:6` HF_MODEL_PATH=${HF_MODEL_PATH:-moonshotai/Moonlight-16B-A3B}
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:8` HF_MODEL_PATH=${HF_MODEL_PATH:-"${RAY_DATA_HOME}/models/Qwen3-VL-235B-A22B-Instruct"}
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:84` HF_MODEL_PATH=${HF_MODEL_PATH:-"Qwen3.5-35B-A3B"}
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:19` HF_MODEL_PATH=${HF_MODEL_PATH:-Qwen/Qwen2.5-Math-7B}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:31` HF_MODEL_PATH=${HF_MODEL_PATH:-"${RAY_DATA_HOME}/models/Qwen3-VL-30B-A3B-Instruct"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
