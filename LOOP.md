# AutoResearch 循环配置

本文件采用 [Loop Engineering](https://github.com/cobusgreyling/loop-engineering) 的控制系统思路，定义一个有状态、有预算、可停止的“实验学习循环”。它不替代 `.planning/STATE.md`：后者记录项目阶段，根目录 `STATE.md` 只记录循环跨运行需要记住的事实与候选动作。

## Active Loop

| Pattern | Trigger | Current level | Goal |
|---|---|---|---|
| Evidence-driven experiment learning | 手动；稳定后可接入 experiment-complete 事件 | L1 report-only | 从最新 run bundle 中提炼一个可验证的下一步，而不是直接改代码 |

主路径：`触发 → 分诊 → 假设 → 人工门 → 隔离执行 → 独立验证 → keep/reject/escalate → 写回状态`。

## L1 输入与输出

输入只读：

- 最新本地 run 的 `manifest.json`、日志、W&B summary、Prometheus 指标与 HTML 报告；
- 当前 `STATE.md`、`loop-run-log.md`、Git diff/commit provenance；
- `.planning/STATE.md` 中已知 blocker 与人工待办。

每次运行只允许输出：

- 一个分层后的问题或机会；
- 一条有证据的候选假设；
- 建议的最小验证动作、风险、预计成本；
- 对 `STATE.md` 和 `loop-run-log.md` 的结构化更新。

L1 禁止改源码、启动远程训练、修改服务或创建 PR。

## Human Gates

以下动作无论循环等级都必须由人批准：

- 远程 NPU/GPU 训练、SSH 配置、BMC/电源操作；
- 凭据、密钥、真实客户配置或 `config/config.yaml` 的变更；
- 修改安全/网络/Compose/CI 配置；
- push、创建 PR、merge、发布或删除任何资源；
- 指标退化但建议“仍然保留”的实验结论。

仓库不允许自动合并。人工决定始终是最终权限边界。

## L2 Worktrees and Verification

只有连续 1–2 周 L1 分诊准确且噪声可接受，才可启用 L2：

1. 一个假设对应一个隔离 worktree；不得把无关修复捆在一起。
2. Maker 只修改已批准范围，并记录命令、diff、run id 与证据路径。
3. 独立 verifier 重新读取目标和 diff，自行运行相称的测试；默认结论为 `REJECT`。
4. 只有 verifier `APPROVE` 且人工批准，才可提议 PR；循环本身不 merge。

## Budget and Circuit Breaker

- L1 每次最多 1 个候选假设，不启动 sub-agent，不运行远程实验。
- L2 每个假设最多 3 次尝试、最多 1 个 maker + 1 个 verifier。
- 同一失败签名连续出现 2 次，判定“无进展”并停止。
- 缺少可比较 baseline、证据不完整、成本上限不明或权限不清时立即停止。
- 发现根目录 `.loop-paused` 时不执行任何动作，只报告暂停原因。
- 完整成本与时限见 `loop-budget.md`；结构化权限见 `loop-constraints.md`。

## State and Run Log

- `STATE.md`：当前高优先级、watch、noise、最近 verdict 和下一人工决定。
- `loop-run-log.md`：不可改写的运行摘要；每次追加时间、输入、判断、动作与停止原因。
- run bundle / manifest 才是实验事实源；`STATE.md` 只保存压缩后的决策上下文。

## Connectors and Least Privilege

- L1 不需要 MCP 写权限；Git/GitHub、W&B、Prometheus 与文件系统均按只读使用。
- L2 如接 GitHub connector，只授予读 CI/issues 和草拟评论所需权限；push/merge 仍由人完成。
- 角色允许的工具范围和 denylist 见 `loop-constraints.md`。

## Escalation Contract

循环必须以 `KEEP`、`REJECT` 或 `ESCALATE_HUMAN` 之一结束。升级给人时必须附上：事实证据、已尝试动作、失败签名、剩余选项、建议选择与预计成本；不得只说“需要人工处理”。
