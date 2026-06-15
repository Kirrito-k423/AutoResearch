---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: MinViable Loop
status: Phase 11 shipped — PR #1
stopped_at: Phase 11 top-level CLI orchestration verified, pushed, and reflected in PR #1; next route is Phase 12 E2E smoke
last_updated: "2026-06-15T16:16:00Z"
last_activity: 2026-06-15
progress:
  total_phases: 13
  completed_phases: 11
  total_plans: 30
  completed_plans: 34
  percent: 85
---

# State: AutoResearch v1.0

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-06 after $gsd-new-project)

**Core value:** "常实践，详记录，知得失，会设计，有整理"——每个 skill 跑一次都留下可被复盘、可被二次开发的产物。

**Current focus:** Phase 11 top-level CLI orchestration is shipped to PR #1; next immediate step is Phase 12 E2E smoke.

## Position

- **Milestone:** v1.0 MinViable Loop
- **Phase:** 12
- **Plan:** Next
- **Last activity:** 2026-06-15

## Session Continuity

- **Last session:** 2026-06-15T10:28:47Z
- **Stopped At:** Phase 11 UAT passed on real run `01KV60QS8PMSEG02MQEB0Z27FT`; branch pushed and PR #1 updated for Phase 11
- **Resume File:** .planning/phases/11-orchestration/11-UAT.md

### Decisions Made This Session (2026-06-15)

- **D-46 workdir 落地**：`ServerSpec.workdir` 默认 `/root`, `--workdir` 可覆盖。
- **D-47 M1 log 拉取边界**：日志走跑后一次性 SFTP 拉取, 实时流留 v1.1。
- **Collect CLI 编排**：`autoresearch collect run` 串 minimal → wandb sync → log collect → prom push → manifest write, 最终 stdout 保持唯一 JSON。
- **Prom push 实现**：远程用 `curl --data-binary` 推 text exposition, 不要求远程安装 `prometheus_client`。
- **D-48 local wandb 修复**：`services/wandb/compose.yml` 去掉 `user: "0"` 并切到新卷 `ar-wandb-data-v2`, 本地 8080 成功完成首次初始化、API key 生成和真实 sync。
- **D-49 services 健康探针修复**：`autoresearch services status` 对 wandb 改查 `/ready`, 避免 nginx 前门存活时的假阳性。
- **验收结论更新**：Phase 8 已完成真实 UAT；A2-AK-225 的 collect run 成功落本地 wandb/log/prom/manifest。
- **D-50 Phase 8 已发 PR**：已创建 GitHub PR `#1 Phase 8: Skill 07 — data-collection`，URL 为 `https://github.com/Kirrito-k423/AutoResearch/pull/1`。
- **D-51 report 真相源**：Phase 9 报告固定从 `manifest.json` 重建 run，全链路 local-first。
- **D-52 report 数据读取边界**：log 读本地 artifact，wandb 读本地 `wandb-summary.json`，Prometheus 读本地服务；不回远端、不依赖云端。
- **D-53 M1 视图语义**：wandb/prom 指标按 snapshot-style 展示，诚实反映 minimal run 的单点数据粒度。
- **D-54 report 交付面**：`autoresearch report render --run-id X [--open]` 生成单文件 `report.html` 并可在本地浏览器打开。
- **D-55 报告链接策略**：raw artifact / W&B / Prometheus 都要给出入口；W&B deep-link best-effort，root URL 保底。
- **D-56 Archon 资产布局**：repo-local `.archon/workflows/` + `.archon/scripts/`，不依赖用户全局资产。
- **D-57 skill workflow 范围**：8 个 skill workflow 包 happy path，不把维护/管理子命令都搬进 Archon。
- **D-58 Archon 输入与 artifact 交接**：`AR_CONFIG_PATH` / `AR_SERVER` / `AR_LIB` / `AR_STACK_LIBS` / `AR_TIMEOUT` / `AR_REMOTE_PROXY_PORT` / `AR_PUSHGATEWAY_URL` / `AR_RUN_ID` 作为覆盖层，`$ARTIFACTS_DIR` 作为节点交接边界。
- **D-59 STACK/COLL loop 表达**：standalone `ar-skill-06` / `ar-skill-07` 保留真实 Archon `loop:`；主 workflow 用 deterministic script 入口保证 smoke run 不依赖 provider auth。
- **D-60 Archon 安装边界**：Archon 继续外部 CLI 管理，不进 `autoresearch services start`；本机需 `archon serve --port 8088`。
- **D-61 主 workflow 端口隔离**：`ar-min-loop` 网络代理默认用远端 `17892`，把 `17890` 留给 reach/wandb。
- **D-62 provider auth 现实边界**：本机 Claude provider 对 loop 节点返回 401；Phase 10 验证 loop YAML 有效，主闭环用 script/bash 节点完成真实端到端。
- **D-63 顶层编排复用边界**：`autoresearch check all` / `run smoke` 复用现有 Python `run_*` 入口，不通过 shell 拼命令。
- **D-64 check all 语义**：`check all` 是 readiness 检查；COLL/RPT 在 8 skill 位置中作为 readiness placeholder，真实执行交给 `run smoke`。
- **D-65 smoke 语义**：`run smoke` 串 collect -> report，任何失败都通过 `failed_step` 和 step diagnosis 指明。
- **D-66 proxy 端口隔离**：`check all` 默认 remote proxy port 使用 `17892`，避免和 reach/wandb 的 `17890` 隧道抢端口。
- **D-67 Prometheus scrape 等待**：`run smoke` 在 collect 推送 Pushgateway 后默认等待 Prometheus 抓到该 run 的指标，再渲染报告。

### Files Created This Session (08-03 / 08-04)

- `datalake/logs/__init__.py`
- `datalake/logs/collector.py`
- `datalake/prometheus/__init__.py`
- `datalake/prometheus/push_gateway.py`
- `datalake/manifest/__init__.py`
- `datalake/manifest/schema.py`
- `datalake/manifest/writer.py`
- `autoresearch/collect/manifest.py`
- `autoresearch/collect/cli.py`
- `tests/test_datalake_logs_collector.py`
- `tests/test_datalake_prometheus_push.py`
- `tests/test_datalake_manifest.py`
- `tests/test_collect_manifest.py`
- `tests/test_collect_cli.py`
- `.planning/phases/08-skill-07-data-collection/08-03-SUMMARY.md`
- `.planning/phases/08-skill-07-data-collection/08-04-SUMMARY.md`
- `.planning/phases/08-skill-07-data-collection/08-UAT.md`

### Verification

- `uv run pytest tests/test_reach_tester.py tests/test_reach_cli.py tests/test_datalake_prometheus_push.py tests/test_collect_cli.py tests/test_datalake_wandb_sync.py tests/test_status.py -q` → 48 passed
- `uv run pytest tests/test_report_loader.py tests/test_report_wandb.py tests/test_report_prometheus.py tests/test_report_render.py tests/test_report_cli.py -q` → 10 passed
- `uv run pytest -q` → 332 passed, 6 warnings
- `uv run autoresearch services status --json` → wandb/prometheus/pushgateway healthy (`3/5` overall; archon/grafana not required for Phase 8)
- `.venv/bin/wandb sync ~/.autoresearch/runs/difdkkcx/wandb` → synced to `http://localhost:8080/autoresearch-local/uncategorized/runs/difdkkcx`
- `uv run autoresearch collect run --server A2-AK-225 --lib verl --config config/config.yaml --timeout 60 --pushgateway-url http://127.0.0.1:17891` → `ok=true`, `run_id=01KV5MV7N5A3RBZ6388E5HCYAP`
- `curl 'http://localhost:9090/api/v1/query?query=autoresearch_npu_count{run_id="01KV5MV7N5A3RBZ6388E5HCYAP"}'` → value `8`
- `uv run autoresearch report render --run-id 01KV5MV7N5A3RBZ6388E5HCYAP` → `ok=true`, `report=/Users/Zhuanz/.autoresearch/runs/01KV5MV7N5A3RBZ6388E5HCYAP/report.html`
- `uv run autoresearch report render --run-id 01KV5MV7N5A3RBZ6388E5HCYAP --open` → `opened=true`
- `CLAUDE_BIN_PATH=/opt/homebrew/bin/claude archon doctor` → all checks passed
- `for wf in ar-skill-01 ... ar-skill-08 ar-min-loop; do archon validate workflows "$wf" --quiet || exit 1; done` → all repo-local workflows valid
- `uv run autoresearch services status --json` → 5/5 healthy, including Archon 8088 and Grafana 3000
- `uv run autoresearch reach test --server A2-AK-225` → `ok=true`, remote can reach local wandb and pushgateway
- `uv run autoresearch stack check --server A2-AK-225 --lib verl` → `ok=true`, 8 NPU one-step dry run
- `CLAUDE_BIN_PATH=/opt/homebrew/bin/claude AR_STACK_LIBS=verl archon workflow run ar-min-loop --no-worktree ""` → completed, Archon run `37dfb89e99e9a482e25fadaf3e5b7d0d`
- `uv run pytest -q` → 352 passed, 6 warnings
- `uv run autoresearch check all --server A2-AK-225 --stack-lib verl` → `ok=true`, 8 steps, 6 passed, 2 warned, 0 failed
- `uv run autoresearch run smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` → `ok=true`, run `01KV60QS8PMSEG02MQEB0Z27FT`, `prometheus_ready=true`, report warnings `[]`

### Decisions Made This Session (2026-06-12)

- **D-32 BMC 密码明文**：用户决定"内网机器密码不加密"，schema 不强制 keyring；`BMCSpec.password` 直接读取
- **D-32 电源 dry-run 双保险**：默认仅返 `would_send`；`--apply` 真打时 `config.bmc.power_operations_allowed` 必须 True
- **D-32 BMC identify 优先级**：UUID > SerialNumber > SKU，第一个非空为 bmc_identifier
- **D-33 sudo_command 显式声明**：默认空字符串（不 sudo），非空则拼到 npu-smi/lspci/driver 命令前
- **A3-AX-176 → A3-AX-180** (ip 192.168.13.180)：同步 config + example
- **A3-AX-153 暂下线**：动态 IP + 宕机中，修好再加
- **A2-AK-102 需 sudo**：user=admin123 + sudo_command="sudo -n"（先 bootstrap NOPASSWD）
- **不引第三方 redfish 库**：用裸 requests + 标准 Redfish REST；iBMC 私有 `/api/` 待协议确认

### Files Created This Session (04-04)

**feat(04-04) commit:**

- `autoresearch/bmc/__init__.py` (27 行) — bmc 模块入口
- `autoresearch/bmc/client.py` (193 行) — Redfish 客户端 (Basic Auth + requests)
- `autoresearch/bmc/identify.py` (131 行) — 双源唯一编码查询
- `autoresearch/bmc/power.py` (161 行) — 电源 dry-run/apply 操作
- `autoresearch/cli.py` (+133 行) — bmc CLI group (identify + power sub-group)
- `autoresearch/hw/models.py` (+3 行) — HardwareData TypedDict 加 3 字段
- `autoresearch/hw/probe.py` (+66/-20 行) — sudo 前缀 + bmc identify 集成
- `config/config.example.yaml` (+74 行) — 4 台 servers 完整配置 + 安全声明
- `tests/test_bmc.py` (205 行) — 12 个 bmc 单元测试
- `tests/test_hw_probe.py` (+286 行) — 3 个 hw 集成测试
- `workspace-core/config/__init__.py` (+2 行) — 导出 BMCSpec
- `workspace-core/config/schema.py` (+35 行) — BMCSpec + sudo_command 字段
- `.planning/phases/04-skill-03-server-hardware-probe/04-04-SUMMARY.md`

### Real-Server UAT 现状

| Server | SSH | hw probe | BMC identify | 阻塞 |
|---|:-:|:-:|:-:|---|
| A2-AK-225 | ✅ | ✅ 8 设备 | ❌ BMC 192.168.12.225 不可达 | 待补 BMC IP |
| A3-AK-182 | ✅ | ✅ 16 设备 | ❌ BMC 192.168.12.182 不可达 | 待 BMC IP/路由修复 |
| A3-AX-180 | ❌ | ❌ ssh_auth | ❌ BMC 192.168.12.180 非 Redfish | 需 key 部署 + BMC 协议 |
| A2-AK-102 | ✅ | ❌ npu_smi_dcmi | ❌ BMC 192.168.12.102 非 Redfish | 需驱动修复 + BMC 协议 |
| A3-AX-153 | — | — | — | 暂下线 (动态 IP) |

## Open Questions

- **iBMC 是否真用 Redfish 还是私有 `/api/`**？决定 `client.py` 是否要写新端点
- **5 台 BMC IP/凭据何时齐**？等齐后跑 04-05 plan (BMC 真机验收)
- **A2-AK-102 NOPASSWD sudo 已配**？未配则 `sudo -n` 会失败，提示用户配

## Active Blockers

- **A3-AX-180 SSH 认证失败**（2026-06-12）— 用户运维事项，需重部署 SSH key
- **A2-AK-102 npu-smi dcmi 故障**（2026-06-12）— 驱动级，需远端调试
- **5 台 BMC iBMC 协议未确认**（2026-06-12）— 待用户确认走 Redfish 还是 `/api/`
- **A3-AX-153 暂宕机**（2026-06-12）— 用户说明动态 IP 修好再加

## Next Steps

1. `$gsd-progress --next` 进入 Phase 12 E2E 端到端 smoke
2. 用 `autoresearch check all` + `autoresearch run smoke` 作为 Phase 12 的本地 CLI 主路径
3. 在 Phase 12 验证报告完整包含 log + wandb + prom 三视图

## Continuation Prompts

```
$gsd-progress --next
```

## Metrics

- **Phases planned:** 13
- **Phases complete:** 11 complete
- **Plans complete:** 34 summaries through Phase 11
- **Requirements:** 88
- **Tests:** 352 / 352 passing
- **Phase 11 UAT:** pass; smoke run `01KV60QS8PMSEG02MQEB0Z27FT`
- **Latest PR:** `#1 Phase 11: Top-level CLI orchestration`

## Branch & Commits

- **Branch:** `codex/phase-02-workspace-core`
- **Latest commit:** `feat(11): add top-level CLI orchestration`
- **Open PR:** `https://github.com/Kirrito-k423/AutoResearch/pull/1`

---
*Last updated: 2026-06-15 after Phase 11 ship to PR #1*
