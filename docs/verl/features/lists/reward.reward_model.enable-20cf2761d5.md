# reward.reward_model.enable

- **参数名**：`reward.reward_model.enable`
- **分类**：算法
- **中文解释**：是否启用单独的 reward model 来为样本打分；示例开启后还配置 reward model 路径和它自己的 rollout 推理后端。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：RewardModelConfig 包含 `enable`、`model_path` 和独立 `rollout` 配置；开启会额外加载/运行奖励模型，增加 GPU 显存、推理延迟和调度资源需求。
- **精度影响**：机制推断：从规则/自定义 reward 切换为模型 reward 会直接改变奖励信号质量与偏差，可能提升偏好对齐，也可能引入 reward hacking 或奖励模型误判。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:71` reward.reward_model.enable=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
