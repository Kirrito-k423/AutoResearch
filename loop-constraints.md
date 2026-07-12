# AutoResearch Loop Constraints

## Role scopes

| Role | Allowed | Not allowed |
|---|---|---|
| Triage | 读 Git、测试结果、run bundle、项目/循环状态；更新循环状态文档 | 改源码、远程命令、外部写入 |
| Maker (L2+) | 仅在批准的 worktree 和路径中编辑；运行批准的测试 | 验证自己的结果、改 denylist、push/merge |
| Verifier | 读目标/diff/证据；独立运行测试；给 verdict | 实现修复、扩大范围、覆盖人工门 |

## Denylist

没有逐次人工批准，不得修改或执行：

- `config/config.yaml`、任何凭据、SSH key、token、keyring 数据；
- BMC 电源操作、破坏性远程命令、容器/数据删除；
- `.github/workflows/**`、`services/**/compose.yml`、网络与安全策略；
- Git push、PR merge、release、tag 或历史重写；
- 跳过/删除测试、降低断言或把失败标记为 expected。

## Allowed L2 change surface

默认只允许人工明确点名的 `autoresearch/**`、`workspace-core/**`、`workspace-adapter/**`、`datalake/**`、`tests/**` 和文档文件。一次循环只允许一个目的清晰的 diff。

## Escalation

以下任一条件触发 `ESCALATE_HUMAN`：权限不清、证据冲突、无 baseline、重复失败、硬件/环境级故障、涉及 denylist、预计超过预算、verifier 无法复现。
