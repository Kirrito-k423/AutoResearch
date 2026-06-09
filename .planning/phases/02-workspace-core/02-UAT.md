---
status: complete
phase: 02-workspace-core
source:
  - 02-01-SUMMARY.md
  - 02-02-SUMMARY.md
  - 02-03-SUMMARY.md
  - 02-04-SUMMARY.md
started: 2026-06-08T02:30:00Z
updated: 2026-06-09T01:32:21Z
---

## Auto-Verified Tests (15 项, agent 跑)

### A1. 全套 pytest 81 PASS
expected: 81 passed in X.Xs (含 phase 1 + 02-01/02/03/04 + 2 gap-closure)
result: pass

### A2. workspace-core 7 子包 import OK
expected: workspace_core.{ssh,secrets,config,progress,log,layout,result} 都能 import 主 API
result: pass

### A3. config: from_yaml 解析 + 中文错误
expected: from_yaml("version: 1") OK; from_yaml("invalid: :") 抛 ConfigError 含 "YAML"
result: pass

### A4. config: 缺必填字段中文错误
expected: from_yaml("servers: [{host: h, user: u}]") 抛 ConfigError 含 "name"
result: pass

### A5. secrets: 软失败 (keyring 不可用 → env fallback)
expected: resolve_secret("<env:HOME>") 返真实 HOME; 缺 env 时抛 SecretError
result: pass

### A6. progress: __AR_PROGRESS__= 写 stderr
expected: emit_progress("test") 抓 stderr 含 "\_\_AR_PROGRESS\_\_=" + JSON payload
result: pass

### A7. layout: ensure_run_dir 创建 logs/wandb/prom
expected: ensure_run_dir("2026-06-08-smoke-001") 创建 3 子目录
result: pass

### A8. layout: run-id 冲突硬失败
expected: 同 run_id 第二次 ensure_run_dir 抛 FileExistsError 含 "已存在"
result: pass

### A9. log: HumanFormatter 含 level + ctx
expected: HumanFormatter 输出含 "INFO" + logger name + ctx dict
result: pass

### A10. log: JsonFormatter 字段完整
expected: JsonFormatter 输出 JSON 含 ts/level/logger/msg
result: pass

### A11. result: merge severity 正确 (FAIL > WARN > OK)
expected: merge([ok(),fail()])=FAIL; merge([ok(),fail(severity=WARN)])=WARN; merge([ok()])=OK
result: pass

### A12. autoresearch ping dummy 模式 JSON stdout
expected: 走 dummy, ssh=true, reverse_tunnel=null, mode=dummy, latency_ms=int
result: pass

### A13. autoresearch ping --lang en 同结构
expected: --lang en JSON 字段不变
result: pass

### A14. autoresearch ping --server nonexistent 返 exit 2
expected: --server 不存在 → exit 2 + 中文错误
result: pass

### A15. 仓文件齐全 (7 子包 + config.example.yaml + 8 PLAN/SUMMARY)
expected: ls 仓根 + .planning 看到所有 02-* 文件
result: pass

## User-Verified Tests (2 项, 需你跑真 SSH)

### U1. autoresearch ping --server nvidia-01 走真 SSH
expected: config.yaml 配 nvidia-01, SSH_PASSWORD_NVIDIA_01 env 设; 命令返 ssh=true, latency_ms 合理
blocked_by: third-party
result: pass
verified: "2026-06-09: uv run autoresearch ping --server A2-AK-225 → ssh=true, exit_code=0, stdout=ok, latency_ms=4331"

### U2. 反向代理: 同命令里 reverse_tunnel=true
expected: 真服务器上 reverse_tunnel 通; 5 秒内能 curl http://localhost:8080 (或类似验证)
blocked_by: third-party
result: pass
verified: "2026-06-09: 同一次真实 ping 建立 remote_port=8080 → local_port=8080，返回 reverse_tunnel=true 后正常停止"

## Summary

total: 17
passed: 17
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — identity_file `~` 展开修复已由单测覆盖，并在 A2-AK-225 真机 SSH + 反向隧道验收通过]
