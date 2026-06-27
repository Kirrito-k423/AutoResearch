# distillation.teacher_models.geo3k.key

- **参数名**：`distillation.teacher_models.geo3k.key`
- **分类**：效率
- **中文解释**：文档说明：Geo3K 教师在多教师 OPD 路由中的标识，必须匹配 `sample[distillation.teacher_key]` 的取值；示例使用 `hiyouga/geometry3k`。
- **常见值**："hiyouga/geometry3k"
- **来源环境变量**：无
- **性能影响**：机制推断：key 本身几乎无性能开销；正确 key 让 Geo3K 样本分发到对应教师副本，错误 key 会导致路由失败或教师资源闲置。
- **精度影响**：文档说明：该 key 决定几何数据样本是否由 Geo3K/VL 教师监督；不匹配会报错或把样本交给错误教师，直接破坏多教师蒸馏标签。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:126` +distillation.teacher_models.geo3k.key="hiyouga/geometry3k"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
