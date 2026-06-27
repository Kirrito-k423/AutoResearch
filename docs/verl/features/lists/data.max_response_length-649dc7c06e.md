# data.max_response_length

- **参数名**：`data.max_response_length`
- **分类**：效率
- **中文解释**：控制 response 最大长度，增大可给模型更多输出空间，但会显著增加 rollout KV cache 和耗时。
- **常见值**：$((1024 * 2))、$((1024 * 20))、$((1024 * 255))、$((1024 * 8))、$max_response_length、1024、2048、256、4096、512、6144、8192
- **来源环境变量**：MAX_RESPONSE_LENGTH、max_response_length
- **性能影响**：机制推断：长度越大，显存、KV cache 和单步/生成耗时通常上升。
- **精度影响**：机制推断：改变有效上下文、输出空间或样本保留策略，可能影响任务准确率。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：79
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
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:64` data.max_response_length=${max_response_length}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:51` data.max_response_length=${max_response_length}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:52` data.max_response_length=${max_response_length}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:89` data.max_response_length=${MAX_RESPONSE_LENGTH}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:55` data.max_response_length=${max_response_length}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
