# data.truncation

- **参数名**：`data.truncation`
- **分类**：效率
- **中文解释**：控制超过 `data.max_prompt_length` 的输入如何处理：从左/右截断，或在严格校验时直接报错。
- **常见值**：'error'、'left'、'right'、error、left
- **来源环境变量**：无
- **性能影响**：文档说明：截断可让长尾 prompt 在固定长度预算内继续训练，`error` 更适合严格校验但会暴露并中断超长样本；真正的算力开销主要由 `max_prompt_length` 与实际 token 数决定。
- **精度影响**：文档说明：左/右截断会丢弃部分上下文；官方 best practices 提到若训练日志出现较大 `clip_ratio` 和指标变差，应增大 `data.max_prompt_length` 或清洗数据。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：85
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:66` data.truncation='error'
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:53` data.truncation='error'
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:54` data.truncation='error'
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:91` data.truncation='error'
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:57` data.truncation='error'

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
