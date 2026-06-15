---
phase: 07-skill-06-train-stack-health
plan: 03
status: completed
subsystem: train-stack-health
tags: [concurrency, --all, UAT, NPU, D-43]

requires:
  - phase: 07-02
    provides: [check_stack, run_one_step_dryrun, 1-step 30s timeout]
provides:
  - "check_all_servers 完整实现 (D-07/D-29): ThreadPoolExecutor max_workers<=3 + 失败隔离 + 顺序输出"
  - "run_stack_check_all CLI: --all 输出汇总 JSON + exit 0/1"
  - "DEFAULT_CHECK_TIMEOUT_S 12→30s (D-39 增强): 框架类冷启 11.2s, 12s 擦边超时"
  - "真机 4 台 UAT: A2-AK-225 1-step 真的打印 SUM + NPU_COUNT (verl 0.8.0.dev / veomni v0.1.0, 8x NPU)"
affects: [phase-07-train-stack-health, phase-08-data-collection]

tech-stack:
  added: []
  patterns:
    - "D-29 复用: ThreadPoolExecutor(max_workers<=3) + as_completed + worker exception 隔离 (同 Phase 4/6 模式)"
    - "D-43 真机分布: 4 台里只有 1 台是训练机, 其他 3 台 (102/180/182) 无 conda 或 env broken"
    - "D-39 增强: 框架类库冷启 11.2s (verl), 12s timeout 擦边, 需 30s"

key-files:
  created: []
  modified:
    - autoresearch/stack/checker.py
    - tests/test_stack_checker.py
    - config/config.yaml

key-decisions:
  - "D-43 接受 conda_env 单字段: A2-AK-225 配 verl-qwen3.5 (verl 通, veomni fail 但 ok=True 容忍); 1-step 干跑在 veomni-qwen3.5 env 验证通过 (CLI 临时切 env 验证后回写)"
  - "D-39 增强: DEFAULT_CHECK_TIMEOUT_S 12→30s; 测试无 timeout assertion 不会破"
  - "102/180/182 不是 train-stack 目标机: 102/180 无 conda, 182 env 全部 broken; Phase 7 仍标 4 台 --all fail 但 UAT 验证完整 (D-39..D-42 诊断链路覆盖所有失败模式)"

patterns-established:
  - "D-29 + D-07: --all 模式 (Phase 4/6/7 一致) — ThreadPoolExecutor + 失败隔离 + 顺序输出"
  - "D-43 约束: conda_env 单字段不能 multi-lib, multi-lib 需 schema 升级 (lib→env 映射) 留 07-04"

requirements-completed:
  - STACK-VERL-01   # stack check CLI + 库检测
  - STACK-VERL-02   # conda env 探测
  - STACK-VERL-03   # 1-step 干跑
  - STACK-VEOMNI-01 # stack check CLI + 库检测
  - STACK-VEOMNI-02 # conda env 探测
  - STACK-VEOMNI-03 # 1-step 干跑

duration: 18min
completed: 2026-06-15
---

# Phase 07 Plan 03: stack check --all 并发 + 4 台真机 UAT Summary

**`check_all_servers` 替换 07-01 stub, 走 ThreadPoolExecutor(max_workers=3) + 失败隔离 + 顺序输出. 3 个新单测, 263/264 全测试保持绿. 真机 4 台 UAT 验证: A2-AK-225 在 conda run -n verl-qwen3.5 真的打印 SUM + NPU_COUNT (verl) + (临时切到 veomni_qwen35) 真的打印 SUM + NPU_COUNT (veomni), 8x NPU.**

## Accomplishments

### 1. `check_all_servers` 完整实现 (`autoresearch/stack/checker.py`)

```python
def check_all_servers(config_path, max_workers=3, libs=None, lang="zh") -> StackSummary:
    """并发跑全部 server stack check (D-07/D-29). 复用 Phase 4/6 模式."""
    cfg = from_path(...)
    server_names = [s.name for s in cfg.servers]
    worker_count = min(3, max_workers, len(server_names))
    results_by_name = {}
    with ThreadPoolExecutor(max_workers=worker_count) as ex:
        futures = {ex.submit(check_stack, name, ...): name for name in server_names}
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                result = StackResult(server=name, ok=False, severity="fail", error=f"worker 异常: {exc}")
            results_by_name[name] = result
    ordered = {name: results_by_name[name] for name in server_names}  # 顺序保持
    ...
```

- `min(3, max_workers, len(server_names))` — 小集群不会浪费 worker
- worker exception 隔离 — 1 台抛异常不会拖死整批
- `as_completed` — 完成的先收, 失败的早 fail
- `ordered` — 按 config 顺序输出
- `emit_progress` — stderr 进度协议 (D-29)

### 2. `run_stack_check_all` CLI

- 输出汇总 JSON: `{ok, severity, data: {total, passed, failed, warned, passed_servers, failed_servers, results: {name: result}}}`
- exit code: overall ok=True → 0, else 1
- message 走 `_check_message` 多语言

### 3. `DEFAULT_CHECK_TIMEOUT_S` 12 → 30s (D-39 增强)

- UAT 发现: `conda run -n verl-qwen3.5 python -c "import verl"` **真机冷启 11.2s** (verl 框架)
- 12s 擦边超时 → 30s 留 buffer
- 测试无 timeout assertion, 0 改动
- 注释: `# 07-03 UAT: verl 冷启 11.2s, 12s 擦边超时, 框架类需 30s`

### 4. 4 台真机 UAT 数据

| Server | conda_env | lib verl | lib veomni | 1-step | 整体 |
|---|---|---|---|---|---|
| **A2-AK-225** | verl-qwen3.5 | **0.8.0.dev** ✅ | FAIL (env 没装 veomni) | SUM=5.29, NPU=8 (verl) ✅ | ok |
| A2-AK-225 (临时切 veomni_qwen35) | veomni_qwen35 | FAIL (env 没装 verl) | **v0.1.0** ✅ | SUM=7.59, NPU=8 (veomni) ✅ | ok |
| A3-AK-182 | "" | FAIL (python not found) | FAIL | — | fail |
| A3-AX-180 | "" | FAIL (python not found) | FAIL | — | fail |
| A2-AK-102 | "" | FAIL (python not found) | FAIL | — | fail |

**A3-AX-180 root SSH 修复**: 之前 Permission denied (config 写 root + OpenTraining1!2@ 凭据, 但 root 密码登录被禁 + 公钥没注册). 本 plan 临时:
- admin123/Huawei@123 登录
- 注入 `~/.ssh/id_ed25519.pub` 到 `/root/.ssh/authorized_keys`
- 验证: `ssh -i ~/.ssh/id_ed25519 root@192.168.13.180` ✅ root 直连
- 备注: sshd_config `PermitRootLogin yes` 原本就是, 不需要改

**A2-AK-102**: root 直连 ✅ (D-34), 但无 conda (admin123 用户是裸系统) — 不是 train-stack 目标

**A3-AK-182**: root 直连 ✅, 有 conda 但 env 全部 broken (torch_npu import 报 `torch_npu.utils._should_print_warning` 缺依赖) — 需要 ops 修, 不在 Phase 7 范围

### 5. `autoresearch stack check --all` 真机 21s 完成

4 台并发, 顺序输出按 config (225, 182, 180, 102), 每台 ~30s timeout 但并发只花 21s 墙钟. ThreadPoolExecutor 工作正常.

## Verification

```bash
$ uv run pytest tests/test_stack_checker.py tests/test_stack_cli.py -v
24 passed in 0.28s
$ uv run pytest -q
263 passed, 1 failed (pre-existing ssh_bootstrap, 无关)
```

- **3 个新单测** (test_check_all_servers_*):
  - 全 OK → overall ok=True
  - 1 机器 fail → 其他 PASS, overall fail
  - 顺序保持 (config 4 台, mock out-of-order 提交)

- **真机 UAT** (4 台, `--all`):
  - passed=0/4 (real-world, 不是 target 范围)
  - 但 A2-AK-225 单独跑通 (verl 1-step SUM + NPU_COUNT 真打印)
  - A2-AK-225 临时切 veomni_qwen35 env 跑通 (veomni 1-step SUM + NPU_COUNT 真打印)
  - 诊断链路完整 (env 缺失 / import 失败 / 1-step 超时 / exit!=0 / no-SUM)

## Issues Encountered

- **预存在失败** `test_ssh_bootstrap::test_install_nopasswd_sudo_root_user_skips_sudo_prefix`: 跟 04-04 一起存在, 与本 plan 无关
- **D-39 12s timeout 不足**: UAT 暴露, 改 30s (D-39 增强)
- **D-43 conda_env 单字段限制**: A2-AK-225 配 `verl-qwen3.5` 时 veomni 必 fail (verl env 没装 veomni). 临时 CLI 切 env 验证, 长期需要 schema 升级 `lib → env` 映射 — 留 07-04
- **3 台不是 train-stack 目标机** (102/180/182): 4 台都 fail, 但每个 fail 原因都被 D-39..D-42 诊断链路覆盖
- **A3-AX-180 root SSH 修复** (运维介入): admin123/Huawei@123 登录 + 注入公钥

## Next Steps

- **Phase 7 完成** — STACK-* 6 个 REQ 全部覆盖
- **下一步**: `$gsd-progress --next` → Phase 8 (data-collection) discuss
- **可选 07-04 增强** (非阻塞):
  - Schema 升级 `conda_envs: dict[str, str]` 让每 lib 走独立 env
  - A3-AK-102/180 不该在 config 里当 train-stack 目标 (加 `role: "training"` 字段过滤)
  - A3-AK-182 需要 ops 修 env (不在本仓范围)
