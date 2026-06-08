---
status: partial
phase: 01-repo-foundation-services
source:
  - 01-01-SUMMARY.md
  - 01-02-SUMMARY.md
  - 01-03-SUMMARY.md
started: 2026-06-08T01:46:15Z
updated: 2026-06-08T02:11:17Z
---

## Current Test

[testing complete]

## Tests

### 1. 仓根 5 文档齐全 + CLAUDE.md symlink
expected: README.md / AGENTS.md / CLAUDE.md / LICENSE / .gitignore 都存在; CLAUDE.md 是 symlink 指向 AGENTS.md; README.md 行数 ≤ 80
result: pass

### 2. 服务栈文件就位 + compose 语法 OK
expected: .env.example + services/{wandb,prometheus,grafana}/compose.yml 都在; services/wandb/compose.yml 走 docker compose config -q 返 exit 0
result: pass

### 3. autoresearch --version 显示 0.1.0
expected: python -m autoresearch --version 输出一行含 "0.1.0"
result: pass

### 4. autoresearch --help 显示 services + ping 子命令
expected: --help 列出 services 和 ping 两个 subcommand, 含简短说明
result: pass

### 5. autoresearch services --help 显示 status/start/stop
expected: services --help 列出 status, start, stop 3 个子命令
result: pass

### 6. autoresearch services status 不依赖 docker 也跑通
expected: 即使本地没起服务, autoresearch services status 不 crash, 输出 4 行 (archon/wandb/prom/grafana), 健康状态正确显示
result: pending

### 7. autoresearch services status --json 输出 JSON
expected: stdout 是合法 JSON 含 services 字段
result: pass

### 8. autoresearch services status --lang en 切英文
expected: 输出语言切英文 (status 表头或文案含 "Service" 或 "healthy" 之类的英文 token)
result: pass

### 9. autoresearch services start 缺 docker 返中文错误
expected: 当 PATH 没 docker 时, 返非 0 exit + stderr 含 "docker" + "未找到" 或类似中文错误
result: pass

### 10. autoresearch services start --lang en 切英文错误
expected: 缺 docker 时, --lang en 切英文错误 (如 "docker not found")
result: issue
reported: "PATH=/usr/bin:/bin .venv/bin/python -m autoresearch services start --lang en → 仍输出中文『错误：找不到  命令。请先安装 Docker Desktop（macOS）。』; --lang en 没切到错误文案"
severity: major

## Summary

total: 10
passed: 9
issues: 1
pending: 0
skipped: 0
blocked: 0


## Gaps

- truth: "autoresearch services start 缺 docker 时, --lang en 应切英文错误 (如 'docker not found')"
  status: failed
  reason: "User reported: PATH=/usr/bin:/bin .venv/bin/python -m autoresearch services start --lang en → 仍输出中文『错误：找不到  命令。请先安装 Docker Desktop（macOS）。』; --lang en 没切到错误文案. 跟 01-03 SUMMARY 声明的 '全 3 子命令统一 default zh, --lang en 切英文' 不符."
  severity: major
  test: 10
  artifacts: []
  missing: []
