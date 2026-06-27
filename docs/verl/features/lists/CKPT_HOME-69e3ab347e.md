# CKPT_HOME

- **参数名**：`CKPT_HOME`
- **分类**：配置
- **中文解释**：SFT/VLM 示例中的 checkpoint 根目录，脚本会创建该目录并传给 `trainer.default_local_dir` 作为本地保存与恢复路径。
- **常见值**：$HOME/open_verl/sft/${project_name
- **来源环境变量**：CKPT_HOME
- **性能影响**：机制推断：路径本身不影响算力；若 checkpoint 目录在慢盘、空间不足或网络文件系统上，会增加保存/恢复耗时并影响端到端训练。
- **精度影响**：机制推断：不直接改变模型更新；但错误路径或恢复到非预期 checkpoint 会改变继续训练起点。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:76` CKPT_HOME=${CKPT_HOME:-$HOME/open_verl/sft/${project_name}/${exp_name}}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
