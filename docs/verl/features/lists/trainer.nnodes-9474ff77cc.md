# trainer.nnodes

- **参数名**：`trainer.nnodes`
- **分类**：效率
- **中文解释**：控制训练任务使用的节点数，通常与 Ray 多节点集群和每节点 GPU/NPU 数共同决定全局可用设备数。
- **常见值**："${NNODES}"、$NODES_NUM、$NUM_NODES、$nnodes、1、12、2、3、4、6、8
- **来源环境变量**：NNODES、TRAIN_NNODES
- **性能影响**：文档说明：官方多节点文档用 `trainer.nnodes` 配合 `trainer.n_gpus_per_node` 提交多节点任务；节点数增加可扩大并行资源，但会带来 Ray 调度、跨节点通信和网络拓扑开销。
- **精度影响**：机制推断：资源规模本身不改变算法目标；只有当同步、全局 batch、随机种子或失败重试改变训练轨迹时才会间接影响结果。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:128` trainer.nnodes=${NNODES}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:95` trainer.nnodes=${NNODES}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:101` trainer.nnodes=${NNODES}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:138` trainer.nnodes=${NNODES}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:123` trainer.nnodes=${NNODES}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
