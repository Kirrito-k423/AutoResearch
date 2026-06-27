# actor_rollout_ref.model.path

- **参数名**：`actor_rollout_ref.model.path`
- **分类**：配置
- **中文解释**：指定模型权重或模型 ID，是模型规模、结构、显存占用和任务能力的来源。
- **常见值**："$MODEL_PATH"、"$STUDENT_MODEL"、"${MODEL_PATH}"、"${RAY_DATA_HOME、"${WORK_DIR、"Qwen3.5-35B-A3B"、$HF_MODEL_PATH、$HOME/models/gpt-oss-20b-bf16、$actor_model_path、${WORK_DIR}、/Qwen3-30B-MoE-merge、ByteDance-Seed/Seed-OSS-36B-Base
- **来源环境变量**：HF_MODEL_PATH、MODEL_DIR、MODEL_PATH
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：80
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:70` actor_rollout_ref.model.path="$MODEL_PATH"
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:57` actor_rollout_ref.model.path="$MODEL_PATH"
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:58` actor_rollout_ref.model.path="$MODEL_PATH"
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:95` actor_rollout_ref.model.path="$MODEL_PATH"
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:61` actor_rollout_ref.model.path="$MODEL_PATH"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
