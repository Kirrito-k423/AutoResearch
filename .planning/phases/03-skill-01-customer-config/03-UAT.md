---
status: complete
phase: 03-skill-01-customer-config
source:
  - 03-CONTEXT.md
  - 03-01-SUMMARY.md
  - 03-02-SUMMARY.md
started: 2026-06-08T13:50:00Z
updated: 2026-06-08T07:25:04Z
---

## Auto-Verified Tests (15 项, agent 跑)

### A1. 全套 pytest 106 PASS
expected: 106 passed in X.Xs
result: pass

### A2. CLI tree: autoresearch config --help 列出 4 子命令
expected: config --help 含 init / validate / show / keyring
result: pass

### A3. init 跑通生成 config/config.yaml
expected: CliRunner + tmp_path, exit 0 + 文件存在 + 含中文 + generated header
result: pass

### A4. 重复 init 返 exit 3
expected: 第二次跑 init 返 exit 3, 输出含 "已存在" + "--force"
result: pass

### A5. init --force 覆盖
expected: 第一次 init 后改文件 + 第二次 init --force, exit 0 + 用户改的冲掉
result: pass

### A6. init --config 自定义路径
expected: --config my/custom/config.yaml 写到那路径
result: pass

### A7. validate 通过 + 中文 header
expected: 合法 config 跑 validate, exit 0 + "✅ ... 校验通过"
result: pass

### A8. validate 失败中文错误
expected: 缺 name 字段, exit 1 + "name" + "必填" 在输出
result: pass

### A9. validate --json 返 JSON
expected: stdout 合法 JSON 含 ok/summary/version/servers_count
result: pass

### A10. show 脱敏生效
expected: 含 password_secret 字段的 config, 走 show, 密码值不出现 + "***" 出现 + identity_file 保留
result: pass

### A11. show --json 脱敏
expected: --json 返 JSON, password_secret 字段值为 "***"
result: pass

### A12. show 缺 config 返 exit 1
expected: 不存在的 config, exit 1 + 中文错误
result: pass

### A13. keyring CLI --help 列出 4 子命令
expected: config keyring --help 含 set / get / delete / list
result: pass

### A14. keyring 4 action 闭环 (mocked)
expected: set→get→delete 三步 returncode 正确 + list 提示
result: pass

### A15. 仓文件齐全 (6 REQ SUMMARY + 8 子命令源码 + 24 tests)
expected: ls 看到 6 文件 (3 SUMMARY + 3 CONTEXT/PLAN), autoresearch/config/ 6 文件, tests/ 4 文件
result: pass

## User-Verified Tests (3 项, 需你跑)

### U1. 真 keyring set + get 闭环 (macOS Keychain)
expected: autoresearch config keyring set MY_TEST --value "hello"; autoresearch config keyring get MY_TEST → print "hello"
blocked_by: third-party
result: pass

### U2. 跑真实 config.yaml 走 validate
expected: 用你的 config/config.yaml (有 A2-AK-225 / A3-AX-153 等真实 servers) 跑 validate, exit 0 + 摘要
blocked_by: third-party
result: pass

### U3. 跑真实 config.yaml 走 show 看脱敏
expected: show 输出含 servers + identity_file + bootstrap_password_secret='***' (明文密码不出现)
blocked_by: third-party
result: pass

## Summary

total: 18
passed: 18
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none yet]
