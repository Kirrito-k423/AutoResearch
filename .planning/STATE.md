---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: MinViable Loop
status: Phase 9 shipped
stopped_at: Phase 9 verified and pushed to PR #1; next route is Phase 10 discuss
last_updated: "2026-06-15T13:45:46Z"
last_activity: 2026-06-15
progress:
  total_phases: 13
  completed_phases: 9
  total_plans: 28
  completed_plans: 29
  percent: 69
---

# State: AutoResearch v1.0

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-06 after $gsd-new-project)

**Core value:** "常实践，详记录，知得失，会设计，有整理"——每个 skill 跑一次都留下可被复盘、可被二次开发的产物。

**Current focus:** Phase 9 experiment-report has been shipped to PR #1; next immediate step is Phase 10 Archon 适配层 discuss/plan.

## Position

- **Milestone:** v1.0 MinViable Loop
- **Phase:** 10
- **Plan:** Discuss
- **Last activity:** 2026-06-15

## Session Continuity

- **Last session:** 2026-06-15T10:28:47Z
- **Stopped At:** Phase 9 UAT passed on real run `01KV5MV7N5A3RBZ6388E5HCYAP` and shipped to the open PR
- **Resume File:** .planning/phases/09-skill-08-experiment-report/09-UAT.md

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

1. `$gsd-progress --next` 进入 Phase 10 Archon 适配层的 discuss/plan/execute
2. 基于已完成的 8-skill CLI 入口，为每个 skill 规划 Archon workflow YAML 包装
3. 视需要把 PR #1 的 review 焦点从 Phase 8 扩展到已并入的 Phase 9 report 能力

## Continuation Prompts

```
$gsd-progress --next
```

## Metrics

- **Phases planned:** 13
- **Phases complete:** 9 complete
- **Plans complete:** 28 / 28 planned-through-Phase-9 (100% code plans); 29 summaries including historical gap-closure work
- **Requirements:** 88
- **Tests:** 332 / 332 passing
- **Phase 9 UAT:** complete, 5 pass / 0 blocked
- **Latest PR:** `#1 Phase 8: Skill 07 — data-collection`

## Branch & Commits

- **Branch:** `codex/phase-02-workspace-core`
- **Latest commit:** `feat(09): add local experiment report workflow`
- **Open PR:** `https://github.com/Kirrito-k423/AutoResearch/pull/1`

---
*Last updated: 2026-06-15 after Phase 9 real UAT completion and PR update prep*
