# trainer.n_gpus_per_node

- **参数名**：`trainer.n_gpus_per_node`
- **分类**：效率
- **中文解释**：控制每个节点参与训练的 GPU/NPU 数，和 `trainer.nnodes` 一起决定 Ray 任务可调度设备总量。
- **常见值**："${NGPUS_PER_NODE}"、"${NPUS_PER_NODE}"、$((8))、$NODE_GPU_NUM、$NUM_GPUS_PER_NODE、$num_gpus_per_node、${GPUS_PER_NODE:-8、${NGPUS_PER_NODE}、1、16、2、4
- **来源环境变量**：NDEVICES_PER_NODE、NGPUS_PER_NODE、NPUS_PER_NODE、TRAIN_NGPUS_PER_NODE
- **性能影响**：文档说明：官方多节点示例直接设置 `trainer.n_gpus_per_node` 与 `trainer.nnodes`；每节点设备数越多，可提升并行吞吐或容纳更大模型，但也可能增加节点内通信和显存分片协调成本。
- **精度影响**：机制推断：设备数本身不改变损失函数；若同时改变全局 batch、并行策略或数值归约顺序，结果可能有间接差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：78
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:127` trainer.n_gpus_per_node=${NGPUS_PER_NODE}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:94` trainer.n_gpus_per_node=${NGPUS_PER_NODE}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:100` trainer.n_gpus_per_node=${NGPUS_PER_NODE}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:137` trainer.n_gpus_per_node=${n_devices_per_node}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:122` trainer.n_gpus_per_node=${NGPUS_PER_NODE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
