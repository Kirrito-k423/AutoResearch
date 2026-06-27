---
name: verl-feature-intelligence
description: 从 Verl examples 脚本和示例 YAML 中维护“可控参数即特性”的中文情报库与 Excel 台账。Use when Codex needs to scan Verl examples/run scripts, extract all user-adjustable parameters and Hydra overrides, create or update per-parameter markdown explanation files under docs/verl/features/lists, use subagents to research unclear parameters from local explanation files, official Verl docs, and repo docs, and produce docs/verl/features/verl-example-parameters.xlsx with parameter name, category, Chinese explanation, common values, performance impact, accuracy impact, and example count.
---

# Verl 示例参数特性情报

把 Verl “特性”优先定义为 examples 脚本里用户能控制的参数旋钮，而不是源码里的内部能力。报告、过程文件、解释文件和 Excel 都必须放在 `docs/verl/features/` 下并用中文呈现。

## 工作流

1. 先确认目标 Verl 仓路径，优先使用本地 checkout，例如 `/Users/Zhuanz/work/github/verl`。
2. 阅读 `references/example-feature-schema.md`，使用其中字段组织参数情报。
3. 阅读 `references/example-source-map.md`，按 examples 脚本优先级采集证据。
4. 从 AutoResearch 仓根运行参数扫描脚本，默认输出到当前 AutoResearch 仓的 `docs/verl/features`。脚本路径按本 skill 目录解析；本机可直接使用绝对路径：

```bash
python3 /Users/Zhuanz/Documents/autoresearch/workspace-adapter/verl-feature-intelligence/scripts/scan_verl_features.py \
  --repo /Users/Zhuanz/work/github/verl
```

5. 对每个参数，先查 `docs/verl/features/lists/<参数名>.md` 是否已有解释；若已有非占位解释，复用并写入 Excel。
6. 对仍是 `待补充` 的参数生成补证批次并启动子代理：

```bash
python3 /Users/Zhuanz/Documents/autoresearch/workspace-adapter/verl-feature-intelligence/scripts/make_research_batches.py \
  --needs docs/verl/features/process/needs-research.txt \
  --out docs/verl/features/process/batches \
  --start 1 \
  --count 6 \
  --batch-size 30
```

7. 子代理只修改自己 batch 参数对应的 `docs/verl/features/lists/*.md`。若文件名经过安全转义，先从 `process/example-parameter-features.json` 按 `parameter` 找 `list_file`。子代理必须按顺序：
   - 搜索 `docs/verl/features/lists/` 是否有同名 markdown 或近似参数解释。
   - 联网搜索 Verl 官方文档。
   - 搜索目标 Verl 仓的 `docs/`。
   - 回写 `docs/verl/features/lists/<参数名>.md`。
8. 每批子代理完成后，重跑扫描脚本吸收解释并刷新 JSON、报告、`needs-research.txt` 和 Excel。
9. 所有参数解释完或保留占位后，输出最终 Excel：`docs/verl/features/verl-example-parameters.xlsx`。
10. 不要把源码内部类名当作特性，除非它被 examples 脚本参数直接暴露。

## 输出目录

固定使用：

```text
docs/verl/features/
  process/
    example-parameter-features.json
    example-parameter-features.md
    needs-research.txt
  lists/
    <参数名>.md
  verl-example-parameters.xlsx
```

## 采集口径

- 优先采集 `examples/**/*.sh` 里的：
  - `FOO=${FOO:-default}` 这类用户可覆盖环境变量。
  - `actor_rollout_ref.*=...`、`data.*=...`、`algorithm.*=...`、`trainer.*=...` 等 Hydra override。
  - `--flag value` 或 `--flag=value` 形式的命令行参数。
  - `ascend_extras`、`profile`、`sft`、`grpo_trainer` 等目录下的特化脚本。
- 可补充采集 `examples/**/*.yaml` 中的运行资源、Ray/SkyPilot 参数和 embedded `python3 -m verl...` 参数。
- CI 与 NPU 只作为证据字段，不作为发现特性的主入口。
- 源码只用于解释某个 examples 参数的含义或确认取值范围，不用于生成主特性列表。

## 分类要求

Excel 中 `分类` 只使用三类：

- `配置`：files、path、name、logger、project、experiment、checkpoint、保存/评测频率等必要文件与运行信息。
- `算法`：学习率、rollout n、KL、entropy、advantage estimator、reward、采样温度/top-p/top-k、训练 epoch/loss 等会改变目标或训练动态的参数。
- `效率`：异步、图模式、BatchSize、micro/mini batch、并行、offload、checkpoint/recompute、显存比例、profiling、资源规模等影响吞吐、显存或调度效率的参数。

## Excel 要求

`docs/verl/features/verl-example-parameters.xlsx` 至少包含这些列：

`参数名 | 分类 | 中文解释 | 常见值 | 性能影响 | 精度影响 | 示例数`

若暂时不知道解释或影响，允许写简单占位符，但必须同时在 `process/needs-research.txt` 中列出，方便后续子代理补证。

## Markdown 要求

报告使用中文，并至少包含：

- `# Verl examples 参数特性报告 YYYY-MM-DD`
- `## 扫描对象`
- `## 参数总览`
- `## 推理/生成参数`
- `## 训练与优化参数`
- `## 并行、显存与调度参数`
- `## 算法与精度参数`
- `## NPU/Ascend 相关参数`
- `## CI 看护与风险`
- `## 下周复核队列`

每个参数解释文件必须包含：

- 参数名
- 分类
- 中文解释
- 常见值
- 性能影响
- 精度影响
- 示例数
- 示例脚本
- 证据片段
- 子代理补证要求

## 判断纪律

- 没有 examples 证据时，不要把某项源码能力列成参数特性。
- 性能/精度影响可分为 `实测`、`文档说明`、`机制推断`、`待补充`。
- NPU 支持只能基于 `ascend_extras`、`npu`、`torch_npu`、`HCCL`、`CANN`、`trainer.device=npu`、NPU profile 脚本或实测日志标注。
- CI 看护只能基于 tests 或 `.github/workflows` 中的脚本/参数引用标注；没有证据写 `未知`。
