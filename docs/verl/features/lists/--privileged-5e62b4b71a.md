# --privileged

- **参数名**：`--privileged`
- **分类**：效率
- **中文解释**：文档说明：Docker 运行参数，用于给容器扩展权限；Verl 安装/Ascend 文档提示应按安全需求评估是否必要，示例注释中也提到它会影响 GPU 自动探测相关行为。
- **常见值**：bypasses
- **来源环境变量**：无
- **性能影响**：机制推断：不直接提升模型计算速度；可能影响容器访问 GPU/NPU 设备、驱动能力或监控接口，从而影响作业能否正常使用硬件。
- **精度影响**：机制推断：容器权限不改变训练目标或数值路径；主要风险是安全边界和设备可见性，而不是精度调参。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:12` # SM>90), and ray_init.num_gpus pinned (Docker --privileged bypasses GPU

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
