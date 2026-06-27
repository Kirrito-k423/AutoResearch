# MODEL_PATH

- **参数名**：`MODEL_PATH`
- **分类**：配置
- **中文解释**：指定模型权重或模型 ID，是模型规模、结构、显存占用和任务能力的来源。
- **常见值**："${RAY_DATA_HOME、"${WORK_DIR、"Qwen/Qwen2.5-7B"、ByteDance-Seed/Seed-OSS-36B-Base、Qwen/Qwen2.5-0.5B-Instruct、Qwen/Qwen2.5-32B、Qwen/Qwen2.5-72B-Instruct、Qwen/Qwen2.5-Math-7B、Qwen/Qwen2.5-VL-7B-Instruct、Qwen/Qwen3-235B-A22B、Qwen/Qwen3-30B-A3B、Qwen/Qwen3-30B-A3B-Base
- **来源环境变量**：MODEL_PATH
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：63
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:11` MODEL_PATH=${MODEL_PATH:-Qwen/Qwen3-30B-A3B-Base}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:8` MODEL_PATH=${MODEL_PATH:-Qwen/Qwen3-8B}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:8` MODEL_PATH=${MODEL_PATH:-Qwen/Qwen3-8B}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:10` MODEL_PATH=${MODEL_PATH:-Qwen/Qwen3-8B}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:11` MODEL_PATH=${MODEL_PATH:-Qwen/Qwen3-30B-A3B-Base}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
