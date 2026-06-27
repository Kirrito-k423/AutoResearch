# actor_rollout_ref.ref.mindspeed.vanilla_mbridge

- **参数名**：`actor_rollout_ref.ref.mindspeed.vanilla_mbridge`
- **分类**：效率
- **中文解释**：文档说明：选择 reference MindSpeed 权重桥接是否使用原始/vanilla mBridge 流程。ref 配置会从 actor 的 MindSpeed mBridge 设置继承，以保持 actor 与 reference 的权重转换路径一致。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：影响 reference 权重转换和 checkpoint 读取路径；与 actor 保持一致可减少额外转换分支，分布式文件系统假设不满足时可能增加 IO 等待或同步失败风险。
- **精度影响**：机制推断：本身不改变算法，但 actor/ref 的 bridge 路径不一致可能造成权重切分或加载口径不同，进而影响 KL/reference logprob。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:155` actor_rollout_ref.ref.mindspeed.vanilla_mbridge=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:166` actor_rollout_ref.ref.mindspeed.vanilla_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
