# data.image_key

- **参数名**：`data.image_key`
- **分类**：效率
- **中文解释**：文档说明：多模态数据集中存放图像的字段名，官方 config 文档说明默认是 `images`，视觉 GRPO/LoRA 示例也将 Geo3K/VL 数据设为 `data.image_key=images`。
- **常见值**：images
- **来源环境变量**：无
- **性能影响**：机制推断：字段名本身不影响吞吐；但启用图像字段意味着数据加载、解码和多模态预处理会增加 CPU/GPU/传输开销。
- **精度影响**：机制推断：字段映射正确才能把图像输入送入多模态模型；键名错误会导致模型缺失视觉信息，显著影响 VL 任务效果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：14
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`
- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:55` data.image_key=images
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:67` data.image_key=images
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:51` data.image_key=images
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:43` data.image_key=images
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:66` data.image_key=images

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
