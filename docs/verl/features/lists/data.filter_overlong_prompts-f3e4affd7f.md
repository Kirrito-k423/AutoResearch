# data.filter_overlong_prompts

- **参数名**：`data.filter_overlong_prompts`
- **分类**：效率
- **中文解释**：控制是否在数据阶段过滤超过长度上限的 prompt；关闭时通常交给 `data.truncation` 的截断或报错策略处理。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：机制推断：开启过滤可减少超长样本进入 tokenization/rollout/训练路径，降低 OOM 或异常风险；但也可能减少有效样本量。
- **精度影响**：机制推断：过滤会改变训练数据分布，尤其会移除长上下文样本；关闭后若依赖截断，则可能保留样本但丢失部分上下文。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：69
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:65` data.filter_overlong_prompts=True
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:52` data.filter_overlong_prompts=True
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:53` data.filter_overlong_prompts=True
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:90` data.filter_overlong_prompts=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:56` data.filter_overlong_prompts=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
