# actor_rollout_ref.model.trust_remote_code

- **参数名**：`actor_rollout_ref.model.trust_remote_code`
- **分类**：效率
- **中文解释**：文档说明：控制是否允许 HuggingFace/Hub 模型仓中的自定义 Python 建模、Tokenizer 或 Processor 代码被加载；Verl examples 在 MiniCPM、Moonlight、MiMo 等需要自定义实现的模型上显式设为 True。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：通常不提升训练或推理吞吐，主要影响模型加载路径；开启后可能增加首次加载/初始化开销与远程代码兼容性风险，后续性能取决于模型自定义实现。
- **精度影响**：机制推断：参数本身不改变训练目标；但若关闭导致自定义模型、Tokenizer 或 Processor 未按预期加载，会改变数据/模型口径甚至无法运行。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:78` actor_rollout_ref.model.trust_remote_code=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:65` actor_rollout_ref.model.trust_remote_code=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:78` actor_rollout_ref.model.trust_remote_code=True
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:52` actor_rollout_ref.model.trust_remote_code=True
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:55` actor_rollout_ref.model.trust_remote_code=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
