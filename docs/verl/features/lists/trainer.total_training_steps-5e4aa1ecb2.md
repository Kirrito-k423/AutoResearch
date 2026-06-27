# trainer.total_training_steps

- **参数名**：`trainer.total_training_steps`
- **分类**：效率
- **中文解释**：文档说明：覆盖 trainer 总训练步数；`null` 时按 `len(train_dataloader) * total_epochs` 自动计算，源码会把该值写入 actor/critic optimizer 调度。
- **常见值**：1、100、200、3000、400、500、50000
- **来源环境变量**：TOTAL_TRAINING_STEPS
- **性能影响**：文档说明：该参数直接决定总运行步数和 checkpoint/验证触发范围；每步吞吐通常不变，但步数越多总训练成本越高。
- **精度影响**：机制推断：训练步数影响优化充分程度以及 lr/weight decay 等 schedule，过少会欠训练，过多可能增加过拟合或策略漂移风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：10
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:133` trainer.total_training_steps=${total_training_steps}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:177` trainer.total_training_steps=${total_training_steps}
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:157` trainer.total_training_steps=500
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:162` trainer.total_training_steps=200
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:112` trainer.total_training_steps=100

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
