# trainer.default_local_dir

- **参数名**：`trainer.default_local_dir`
- **分类**：配置
- **中文解释**：文档说明：本地 checkpoint 保存根目录；官方 checkpoint 文档说明它通常作为 `checkpoints/${trainer.project_name}/${trainer.experiment_name}` 前缀，下面按 global step 保存 actor/critic 分片、优化器和额外状态。
- **常见值**："${CKPTS_DIR}"、"${CKPT_HOME}"、"${RAY_DATA_HOME、"${ckpts_home}"、"${save_path}"、"Qwen/Qwen3.5-122B/verl_checkpoint"、$CKPT_DIR、$save_path、/root/checkpoints/Qwen2.5-Math-7B
- **来源环境变量**：CKPTS_DIR、SAVE_PATH、save_path
- **性能影响**：机制推断：目录本身不影响计算吞吐，但落在慢盘/网络盘会放大 save/load checkpoint 的 I/O 时间；路径不可写会导致保存失败。
- **精度影响**：机制推断：不直接影响精度；但可靠的 checkpoint 路径影响故障恢复和继续训练的一致性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：25
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:150` trainer.default_local_dir="${CKPTS_DIR}" \
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:180` trainer.default_local_dir="${CKPTS_DIR}"
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:154` trainer.default_local_dir=${ckpts_dir}
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:183` trainer.default_local_dir="${CKPTS_DIR}"
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:110` trainer.default_local_dir=$CKPT_DIR

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
