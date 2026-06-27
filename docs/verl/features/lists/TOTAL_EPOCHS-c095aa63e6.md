# TOTAL_EPOCHS

- **参数名**：`TOTAL_EPOCHS`
- **分类**：算法
- **中文解释**：示例脚本中的总训练 epoch 数环境变量，通常传入 `trainer.total_epochs` 控制训练循环轮数。
- **常见值**：1、10、1000、15、2、5
- **来源环境变量**：TOTAL_EPOCHS
- **性能影响**：文档说明：quickstart 和多节点示例直接设置 `trainer.total_epochs`；增大该值通常近似线性增加端到端训练时长和 checkpoint/评测机会。
- **精度影响**：机制推断：训练轮数增加通常给模型更多优化机会，但过多可能过拟合、策略漂移或放大 reward hacking；过少可能欠训练。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：56
- **需要子代理补证**：否

## 示例脚本

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
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:44` total_epochs=${TOTAL_EPOCHS:-10}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:27` total_epochs=${TOTAL_EPOCHS:-15}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:28` total_epochs=${TOTAL_EPOCHS:-15}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:31` TOTAL_EPOCHS=${TOTAL_EPOCHS:-10}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:36` total_epochs=${TOTAL_EPOCHS:-10}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
