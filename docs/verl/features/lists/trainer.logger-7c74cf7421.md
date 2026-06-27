# trainer.logger

- **参数名**：`trainer.logger`
- **分类**：配置
- **中文解释**：训练指标日志后端列表；Verl `Tracking` 支持 console、wandb、swanlab、mlflow、tensorboard、trackio、file 等后端，examples 常用 `["console","wandb"]`。
- **常见值**：'["console", "wandb"]'、'["console","tensorboard","file"]'、'["console","tensorboard"]'、'["console","wandb","file"]'、'["console","wandb"]'、'["console"]'、['console','tensorboard']、['console','wandb']、[console,wandb]、console
- **来源环境变量**：无
- **性能影响**：机制推断：console 开销较小；启用 wandb/mlflow/tensorboard/trackio/file 会增加序列化、磁盘或网络写入，日志量大时可能拉长端到端训练时间。
- **精度影响**：机制推断：只改变指标记录位置，不改变训练目标或梯度；主要影响可观测性、复现实验排查和模型选择依据。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：93
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
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:124` trainer.logger='["console","wandb"]'
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:91` trainer.logger='["console","wandb"]'
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:97` trainer.logger='["console","wandb"]'
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:134` trainer.logger='["console","wandb"]'
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:119` trainer.logger='["console","wandb"]'

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
