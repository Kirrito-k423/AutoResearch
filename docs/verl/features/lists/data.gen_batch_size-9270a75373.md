# data.gen_batch_size

- **参数名**：`data.gen_batch_size`
- **分类**：效率
- **中文解释**：文档说明：生成/采样阶段使用的 batch size；DAPO 文档说明 trainer 会用 `gen_batch_size` 重复采样，直到凑够合格 group 或达到 `max_num_gen_batches`。fully_async 示例中该值固定为 1。
- **常见值**：1
- **来源环境变量**：GEN_BATCH_SIZE
- **性能影响**：文档说明：增大 `gen_batch_size` 可提高一次采样覆盖量和 rollout 批量效率，但会增加瞬时显存、队列和过滤开销；fully_async rollouter 源码当前要求 `gen_batch_size == 1`。
- **精度影响**：机制推断：本身不改变 reward 或 loss，但在 DAPO/group filtering 中会改变候选样本池和合格组分布，进而影响训练信号；fully_async 下主要影响样本生产节奏。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:72` data.gen_batch_size=${gen_batch_size} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
