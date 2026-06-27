# trainer.default_hdfs_dir

- **参数名**：`trainer.default_hdfs_dir`
- **分类**：配置
- **中文解释**：远端 HDFS checkpoint 根目录；配置文档默认 `null`，保存逻辑在非空时会把 actor/critic checkpoint 的远端路径拼到该目录下，`null` 表示只使用本地默认目录。
- **常见值**：null
- **来源环境变量**：无
- **性能影响**：文档说明：非空时 checkpoint 保存会额外创建/拷贝到 HDFS，增加网络与 HDFS I/O 开销；`null` 可避免远端上传，但少一份远端容灾副本。
- **精度影响**：机制推断：不参与训练计算；主要影响 checkpoint 持久化、恢复和容灾，HDFS 保存失败影响继续训练而非单步精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-ppo.yaml:91` trainer.default_hdfs_dir=null \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
