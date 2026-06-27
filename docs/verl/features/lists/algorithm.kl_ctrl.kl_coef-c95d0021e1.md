# algorithm.kl_ctrl.kl_coef

- **参数名**：`algorithm.kl_ctrl.kl_coef`
- **分类**：算法
- **中文解释**：文档说明：in-reward KL penalty 的初始/固定系数，属于 `algorithm.kl_ctrl`，用于把策略相对参考模型的 KL 惩罚加入 reward，而不是 actor loss。
- **常见值**：$kl_coef、0.0、0.001
- **来源环境变量**：KL_COEF、KL_LOSS_COEF
- **性能影响**：机制推断：系数本身几乎不影响吞吐；若启用 in-reward KL，需要计算 reference/old policy log-prob，相关 forward 才是主要开销。
- **精度影响**：文档说明：调大表示更强惩罚策略偏离，通常提升稳定性但压缩探索和奖励优化空间；调小则相反。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：19
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/remax_trainer/run_qwen2.5_math_7b_sync_fsdp.sh`
- `examples/remax_trainer/run_qwen3_8b_fsdp.sh`
- `examples/rloo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:76` algorithm.kl_ctrl.kl_coef=0.0 \
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:47` algorithm.kl_ctrl.kl_coef=${KL_LOSS_COEF}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:176` algorithm.kl_ctrl.kl_coef=${kl_coef}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:69` algorithm.kl_ctrl.kl_coef=0.0
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:131` algorithm.kl_ctrl.kl_coef=$kl_coef

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
