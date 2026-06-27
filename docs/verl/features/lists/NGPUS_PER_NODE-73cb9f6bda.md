# NGPUS_PER_NODE

- **参数名**：`NGPUS_PER_NODE`
- **分类**：效率
- **中文解释**：示例脚本中的每节点 GPU 数环境变量，通常传入 `trainer.n_gpus_per_node`。
- **常见值**：${GPUS_PER_NODE:-8、2、4、8
- **来源环境变量**：NGPUS_PER_NODE
- **性能影响**：文档说明：PPO/GRPO README 和多节点文档都展示通过 `NGPUS_PER_NODE`/`trainer.n_gpus_per_node` 调整资源；增大可提升并行容量，但受节点内互联、显存和并行策略约束。
- **精度影响**：机制推断：资源变量不直接改变目标函数；若同步 batch、并行切分或数值归约路径随之变化，可能产生间接差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：50
- **需要子代理补证**：否

## 示例脚本

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
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:13` NGPUS_PER_NODE=${NGPUS_PER_NODE:-8}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:10` NGPUS_PER_NODE=${NGPUS_PER_NODE:-8}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:10` NGPUS_PER_NODE=${NGPUS_PER_NODE:-8}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:13` NGPUS_PER_NODE=${NGPUS_PER_NODE:-8}
- `examples/otb_trainer/run_qwen3_8b_fsdp.sh:9` NGPUS_PER_NODE=${NGPUS_PER_NODE:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
