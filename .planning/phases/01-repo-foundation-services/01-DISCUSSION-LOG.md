# Phase 1: 仓骨架与本地服务栈 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-06
**Phase:** 01-仓骨架与本地服务栈
**Areas discussed:** README 调性, AGENTS/CLAUDE 分工, 本地服务编排, CLI 入口, Archon 集成

---

## README 调性与深度

| Option | Description | Selected |
|--------|-------------|----------|
| A) 极简宣言 | ≤ 1 屏：哲学 + 1 行 quickstart + LICENSE 链接 | ✓ |
| B) 标准 README | 2-3 屏：哲学 + 架构图 + 8 步循环 + quickstart + 目录结构 | |
| C) 详细 README | 多屏：含 FAQ、Roadmap 链接、Contributing、ChangeLog 摘要 | |

**User's choice:** A) 极简宣言
**Notes:** 用户选 A 的原因：M1 阶段够用即可；详细文档（FAQ / Contributing / ChangeLog）放到 M1 完结时一起加。

**Follow-up lock:** README ≤ 80 行；含哲学 + 1 行 quickstart + 架构图链接 + 8 步循环链接 + LICENSE；不放 badges / FAQ / Contributing / Changelog。

---

## AGENTS.md / CLAUDE.md 分工

| Option | Description | Selected |
|--------|-------------|----------|
| A) 单 AGENTS.md | CLAUDE.md 用 symlink 指向 AGENTS.md（单源真相） | ✓ |
| B) 双份不重叠 | AGENTS.md 写"仓级约定"，CLAUDE.md 写"Claude 特定技巧" | |
| C) 只写 CLAUDE.md | M1 阶段只针对 Claude，AGENTS.md 留空 | |

**User's choice:** A) 单 AGENTS.md
**Notes:** 用户希望单源真相；symlink 用相对路径（git 可追踪，跨机器不坏）。

**Follow-up lock:** 写一份 `AGENTS.md`（含 8 步循环 / 三沉淀层 / 进度协议 / 测试规范）；`CLAUDE.md` 是 `AGENTS.md` 的相对路径 symlink。

---

## 本地服务编排粒度

| Option | Description | Selected |
|--------|-------------|----------|
| A) 单 docker-compose.yml | 4 服务同 network，统一启停 | |
| B) base + override | `docker-compose.yml` 基础 + `docker-compose.override.yml` 开发覆盖 | |
| C) 每服务一个 compose | 完全解耦，靠 `ar-services start` 串起 | ✓ |

**User's choice:** C) 每服务一个 compose
**Notes:** 用户倾向"完全解耦"，每个服务一个独立 compose 文件 + README；`autoresearch services start` 串行调起。

**Follow-up lock:** 4 个 `services/<name>/compose.yml`；`autoresearch services start` 走 `docker compose -f services/X/compose.yml up -d` 串行；`status` 并发查 4 服务 healthz；端口固定 wandb 8080 / Prom 9090 / Grafana 3000 / Archon 8088。

---

## CLI 入口形状

| Option | Description | Selected |
|--------|-------------|----------|
| A) 单体 `autoresearch` | 一个二进制，所有子命令（`autoresearch services status`） | ✓ |
| B) 多 `ar-*` 二进制 | 每个 skill 一个（`ar-services`、`ar-config`） | |
| C) 单体 + 别名 | 主入口 `autoresearch`，skill 同时暴露 `ar-X` 短名 | |

**User's choice:** A) 单体 `autoresearch`
**Notes:** 用户选 A — 单二进制所有子命令；不需要"每个 skill 独立二进制"那种极致的解耦。

**Follow-up lock:** Python `click` 框架；`autoresearch/__main__.py` + `autoresearch/cli.py` 入口；`[project.scripts]` 暴露 `autoresearch` 命令；M1 阶段只实现 `autoresearch services {status,start,stop}`。

---

## Archon 集成方式

| Option | Description | Selected |
|--------|-------------|----------|
| A) 全局 `archon` 独立 | 装 `archon` CLI 到 PATH，Compose 不管 Archon | ✓ |
| B) Archon 容器化进 compose | 我们的 compose 里直接 include Archon image | |
| C) Archon + 包装子命令 | Archon 仍独立装，但 `autoresearch archon {up,down,status}` 包装 | |

**User's choice:** A) 全局 `archon` 独立
**Notes:** 用户选 A — Archon 单独装 + `archon serve` 起；我们的 compose 只管 3 个服务。

**Follow-up lock:** Archon 不在我们的 compose 里；`services/archon/` 只有 README 指向 archon.diy；`autoresearch services status` 仍查 4 服务（Archon 走 `http://localhost:8088/healthz`）；`autoresearch services start` 起 3 compose 服务，输出明确"Archon 由 `archon serve` 自行管理"。

---

## 一致性检查：SVC-01 vs 5A

**问题：** REQUIREMENTS.md 原 SVC-01 写 "`docker-compose.yml` 起 Archon server"；5A 决定 Archon 不在我们的 compose 里。

**解决：** 修订 SVC-01 为：

> SVC-01 — Archon 启动由 `archon serve` 控制（不在我们的 docker-compose 里），需单独安装 `archon` CLI 到 PATH

下游 SVC-CHK-* REQ 无需改。

---

## the agent's Discretion

| 领域 | 状态 |
|---|---|
| CLI 错误信息中英混杂（默认中文，--lang en 切英文） | 自由决定 |
| 单测 vs 集测的覆盖比例 | M1 阶段 01 可只做单测 |
| `start.sh` 脚本的存在与否 | 自由决定 |
| Python 包管理工具（pip / uv / poetry） | 自由决定（建议 uv，与现代 Python 栈一致） |

---

## Deferred Ideas

- **多用户/多租户** — M2+；Phase 1 单用户单本机
- **Web UI 自研** — 复用 Archon Web UI + wandb + Grafana，不造轮子
- **CI/CD** — Phase 1 不配置 GitHub Actions；M1.1 再说
- **服务 TLS** — 本地 localhost，不上 TLS
- **多 docker-compose profile（dev/prod）** — M1 只有 dev 配置
- **多语言 CLI 错误信息** — M1 单中文足够

