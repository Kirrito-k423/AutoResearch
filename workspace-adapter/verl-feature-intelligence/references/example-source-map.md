# Examples 参数采集路径

## 优先级

1. `examples/**/*.sh` 中明确标注 user-adjustable、Knobs 或参数数组的脚本。
2. `examples/ascend_extras/**/*.sh`、`examples/profile/**/*npu*.sh` 等 NPU/Ascend 专用脚本。
3. `examples/**/*.yaml` 中的 SkyPilot、Ray、资源和 embedded `python3 -m verl` 参数。
4. `docs/examples` 或示例 README 中对参数的解释。
5. `tests/` 和 `.github/workflows/` 中对 examples 或参数的引用，用于判断 CI 看护。
6. 源码实现，仅用于解释参数含义或确认取值范围。

## 推荐扫描目录

- `examples/grpo_trainer/`
- `examples/ppo_trainer/`
- `examples/sft/`
- `examples/ascend_extras/`
- `examples/profile/`
- `examples/tuning/`
- `examples/tutorial/skypilot/`
- `examples/*_trainer/`

## 分类提示

- 配置：`train_files`、`val_files`、`model.path`、`MODEL_PATH`、`project_name`、`experiment_name`、`logger`、checkpoint 路径、保存/评测频率。
- 算法：`optim.lr`、`ACTOR_LR`、`rollout.n`、`ROLLOUT_N`、`adv_estimator`、`kl_loss_coef`、`entropy_coeff`、`temperature`、`top_p`、`top_k`、reward/loss 相关参数。
- 效率：`train_batch_size`、`micro_batch`、`mini_batch`、`tensor_model_parallel_size`、`pipeline_model_parallel_size`、`context_parallel_size`、`offload`、`checkpointing`、`recompute`、`gpu_memory_utilization`、`async`、`compile`、`profiler`、资源规模。

## 不理解参数的补证顺序

1. 搜索 `docs/verl/features/lists/<参数名>.md` 或近似文件。
2. 联网搜索 Verl 官方文档。
3. 搜索目标 Verl 仓的 `docs/`。
4. 回写 `docs/verl/features/lists/<参数名>.md`。
5. 重新生成 `docs/verl/features/verl-example-parameters.xlsx`。

## 周报复核清单

- 本周新增/修改了哪些 examples 脚本？
- Top 参数是否来自 examples，而不是源码关键词？
- 参数默认值是否来自脚本中的真实赋值？
- NPU 支持是否有 NPU 专用 examples 或实测证据？
- CI 看护是否有 tests/workflows 证据？
- 对性能/精度的影响是否标注“机制推断”或更强证据？
