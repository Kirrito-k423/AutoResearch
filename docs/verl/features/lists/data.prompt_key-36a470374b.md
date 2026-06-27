# data.prompt_key

- **参数名**：`data.prompt_key`
- **分类**：配置
- **中文解释**：文档说明：数据集中 prompt 字段名，官方配置文档说明默认 `prompt`；RL dataset 会用该字段构造模型输入。
- **常见值**："prompt"、prompt
- **来源环境变量**：无
- **性能影响**：机制推断：仅影响数据列选择，通常不直接影响吞吐；所选字段文本更长会通过 token 数增加显存和延迟。
- **精度影响**：机制推断：字段错误会把错误文本送入模型或导致加载失败，直接影响训练/评测有效性；字段正确时只是数据 schema 适配。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:67` data.prompt_key=prompt \
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:40` data.prompt_key="prompt"
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:97` data.prompt_key=prompt
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:119` data.prompt_key=prompt
- `examples/generation/run_deepseek_llm_7b.sh:32` data.prompt_key=prompt \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
