# trainer.val_before_train

- **参数名**：`trainer.val_before_train`
- **分类**：配置
- **中文解释**：文档说明：控制训练开始前是否先跑一次验证，用于获得 baseline checkpoint/初始指标；examples 中常按是否需要起始评测设为 True 或 False。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：设为 True 会在第一个训练 step 前额外执行一次验证，增加启动时间和一次评测的 rollout/推理开销。
- **精度影响**：机制推断：不改变训练目标；但初始验证能暴露数据、reward 或采样配置问题，间接降低误跑风险。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：36
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:129` trainer.val_before_train=False
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:160` trainer.val_before_train=False
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:124` trainer.val_before_train=False
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh:111` trainer.val_before_train=False
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh:98` trainer.val_before_train=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
