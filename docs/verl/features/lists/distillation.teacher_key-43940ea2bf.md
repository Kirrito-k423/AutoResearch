# distillation.teacher_key

- **参数名**：`distillation.teacher_key`
- **分类**：效率
- **中文解释**：文档说明：OPD 多教师蒸馏中用于路由样本的字段名；默认 `data_source`，每个样本的 `sample[teacher_key]` 必须匹配某个 teacher 的 `key`。
- **常见值**：data_source
- **来源环境变量**：无
- **性能影响**：机制推断：路由字段本身开销很小；配置正确可把不同数据源分发到对应教师服务，配置错误会导致查找失败或只使用单教师路径。
- **精度影响**：文档说明：多教师模式下该字段决定样本使用哪个教师计算 logprob；若 `teacher_key` 或 teacher `key` 不匹配，会路由到错误教师或报错，直接影响蒸馏监督质量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:116` distillation.teacher_key=data_source

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
