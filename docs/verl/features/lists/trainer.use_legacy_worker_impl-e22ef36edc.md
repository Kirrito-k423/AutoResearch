# trainer.use_legacy_worker_impl

- **参数名**：`trainer.use_legacy_worker_impl`
- **分类**：效率
- **中文解释**：文档说明：控制是否使用旧版 worker 实现；Verl engine workers 文档说明旧版 worker 实现已移除、当前仅保留 unified engine，示例中 `disable` 表示显式禁用旧实现路径。
- **常见值**：disable
- **来源环境变量**：无
- **性能影响**：文档说明：统一 worker/engine 路径会影响执行编排和兼容性；禁用 legacy 路径通常不作为吞吐调参旋钮，主要避免走已移除或不兼容实现。
- **精度影响**：机制推断：worker 实现选择不改变算法目标；若 legacy/统一实现存在兼容性差异，影响通常表现为运行失败或调度差异，而非有意改变精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:102` +trainer.use_legacy_worker_impl=disable

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
