# Loop Safety

AutoResearch 的循环默认运行在 L1 report-only。结构化权限、denylist 和人工升级条件以根目录
[`loop-constraints.md`](../loop-constraints.md) 为准；预算与 kill switch 以
[`loop-budget.md`](../loop-budget.md) 为准。

## 固定安全边界

- 不自动 merge、release、tag 或改写 Git 历史。
- L1 不改源码、不跑远程命令、不写外部系统。
- 远程训练、BMC/电源、凭据、网络与服务配置始终需要人工逐次批准。
- L2 的 maker 与 verifier 必须分离；verifier 不实现修复。
- 同一失败签名两次或同一假设三次失败后停止并升级。
- `.loop-paused` 或 `STATE.md: Status: paused` 是硬 kill switch。

## Connector scope

L1 只读。L2 如启用 GitHub/MCP，最多读取 CI/issues 和草拟评论；push、merge 与对外发布不授予循环。
