# distillation.teacher_models.geo3k.inference.name

- **参数名**：`distillation.teacher_models.geo3k.inference.name`
- **分类**：配置
- **中文解释**：on-policy distillation 多教师配置中 Geo3K/VL 教师模型的推理后端名称；示例设为 `vllm`，用于让该教师通过 vLLM 产生蒸馏信号。
- **常见值**：vllm
- **来源环境变量**：无
- **性能影响**：机制推断：教师推理后端决定 Geo3K 教师侧吞吐、显存管理和并行能力；`vllm` 通常用于提升批量推理效率，但需要相应显存和兼容性。
- **精度影响**：机制推断：后端名称不改变蒸馏 loss 定义；不同后端的采样、dtype、logprob 或多模态支持差异可能带来小幅数值/行为差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:129` +distillation.teacher_models.geo3k.inference.name=vllm

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
