---
phase: 01
slug: repo-foundation-services
confidence: HIGH
researched: 2026-06-06
---

# Phase 1: 仓骨架与本地服务栈 — Research

**Researched:** 2026-06-06
**Domain:** Python CLI + Docker Compose orchestration for local dev services
**Confidence:** HIGH

<user_constraints>
## User Constraints (from 01-CONTEXT.md)

### Locked Decisions (D-01..D-06)
- **D-01:** README.md ≤ 80 行；纯宣言式（哲学 + 1 行 quickstart + LICENSE 链接 + 文档引用）；不放 badges/FAQ/Contributing/Changelog
- **D-02:** 写一份 `AGENTS.md`（仓约定 / 8 步循环 / 三沉淀层 / 进度协议 / 测试规范）；`CLAUDE.md` 是 `AGENTS.md` 的相对路径 symlink（单源真相）
- **D-03:** 4 个 `services/<name>/compose.yml`；`autoresearch services start` 串行 `docker compose -f services/X/compose.yml up -d`；端口固定 wandb 8080 / Prom 9090 / Grafana 3000 / Archon 8088
- **D-04:** Python `click`；`autoresearch/__main__.py` + `[project.scripts]` 暴露 `autoresearch`；M1 阶段只实现 `services {status,start,stop}`
- **D-05:** Archon **不**在我们的 docker-compose；`services/archon/` 只有 README 指向 archon.diy；`autoresearch services status` 仍查 4 服务
- **D-06:** REQUIREMENTS.md SVC-01 修订为「Archon 启动由 `archon serve` 控制，需单独安装 `archon` CLI 到 PATH」

### the agent's Discretion
- CLI 错误信息的中英混杂（默认中文，--lang en 切英文）
- 单测 vs 集测的覆盖比例（M1 阶段 01 可只做单测）
- `start.sh` 脚本的存在与否
- Python 包管理工具（pip / uv / poetry）—— **建议 uv**

### Deferred Ideas (OUT OF SCOPE)
- 多用户/多租户
- Web UI 自研
- CI/CD（GitHub Actions）
- 服务 TLS
- 多 docker-compose profile（dev/prod）
- 多语言 CLI 错误信息
</user_constraints>

<architectural_responsibility_map>
## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| 仓根文档 (README/AGENTS/LICENSE) | Repo root (meta) | — | 静态元信息；面向协作者 |
| Docker Compose 服务编排 | Local container runtime | — | docker-compose 是本地单机服务编排的事实标准 |
| Python CLI 入口 (`autoresearch`) | Local dev environment | — | 终端调用；与本机 Docker CLI 交互 |
| 服务 healthz 探测 (HTTP) | Local network | — | localhost 跨容器/本机探测 |
| 进度协议 `__AR_PROGRESS__=...` | Stdout/stderr (CLI) | — | 通用协议；Phase 2 才用，Phase 1 预留接口 |
</architectural_responsibility_map>

<research_summary>
## Summary

Phase 1 交付一个能 `git clone && cd autoresearch && docker compose up -d && autoresearch services status` 全绿的最简骨架。所有服务在本地 Mac 跑（Docker Desktop 已假设安装），不涉及远端 NPU 服务器或 SSH。

**关键技术决策（基于 D-01..D-06）：**
- 服务编排用 **Docker Compose v2 plugin**（Mac/Win/Linux 内置）而非旧版 `docker-compose` 二进制
- Archon **不进** compose；走 `archon serve` 单独进程
- CLI 用 **Python click 8.x**（PROJECT.md 锁定）+ uv 管理包
- 4 服务 healthz 全部走 HTTP GET，状态码 2xx = healthy
- `autoresearch services start` 用 `subprocess.run` 串行调 3 个 compose 文件，避免端口竞争

**Primary recommendation:** 单包 `autoresearch/` Python 模块 + 4 个独立 `services/<name>/compose.yml` + 顶层元文档（README/AGENTS/CLAUDE/LICENSE/.gitignore）。三件大事并行（仓根文档 / 服务编排 / CLI），可走 Wave 1 三 plan 并行。
</research_summary>

<standard_stack>
## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| click | 8.1.x | CLI 框架 | PROJECT.md 锁定；装饰器风格简洁；可树状子命令 |
| requests | 2.31+ | HTTP client (healthz) | 行业标准；sync 阻塞调用对 status 命令足够 |
| Docker Compose v2 | ≥ 2.20 | 服务编排 | 2024 年起 Docker Desktop 默认；`docker compose` 子命令而非独立 binary |
| Python | 3.11+ | 运行时 | PROJECT.md 锁定；与 verl/veomni 对齐 |
| uv | 0.4+ | 包管理 | 比 pip/poetry 快 10x；lockfile 原生支持；Astral 维护 |
| pytest | 8.x | 测试 | PROJECT.md 锁定 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| concurrent.futures (stdlib) | — | ThreadPool 并发探测 | 4 个 healthz 并发查；`requests` 是阻塞 IO |
| ruamel.yaml / PyYAML | 6.x | 配置/manifest 读写 | M1 Phase 1 暂不需要；为 Phase 2 CORE-CFG 预留 |
| rich | 13.x | 美化 stdout | 可选；M1 阶段人读为主 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| click | typer / argparse | click 更稳定；typer 依赖 type hints 在重写 CLI 时反而啰嗦 |
| requests | httpx / aiohttp | async 在 M1 不必要；requests 简单 |
| Docker Compose v2 | docker-compose v1 | v1 已弃用；v2 是 Docker CLI 子命令 |
| uv | poetry / pip-tools | uv 速度快；lockfile 比 pip-tools 简单 |

**Installation:**
```bash
# uv init 流程（M1 推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init --package autoresearch
uv add click requests pytest
```

### 服务镜像版本
| 服务 | 镜像 | Tag | 端口 | 配置文件 |
|------|------|-----|------|----------|
| Archon | (本地 CLI，无 image) | — | 8088 | N/A |
| wandb (local) | `wandb/local` | `0.17.5` | 8080 | — |
| Prometheus | `prom/prometheus` | `v2.51.0` | 9090 | `prometheus.yml` (self-scrape) |
| Grafana | `grafana/grafana` | `10.4.0` | 3000 | `datasources.yml` (provisioning) |
</standard_stack>

<architecture_patterns>
## Architecture Patterns

### 系统架构图（数据流视角）

```
[User Terminal]
    │
    │ $ autoresearch services status
    ▼
[autoresearch CLI (Python/click)]
    │
    │ for each service in [archon, wandb, prometheus, grafana]:
    ▼
[HTTP GET /healthz or /-/healthy] ─── concurrent.futures.ThreadPoolExecutor (4 workers)
    │
    ├─ archon:    http://localhost:8088/healthz
    ├─ wandb:     http://localhost:8080/healthz
    ├─ prom:      http://localhost:9090/-/healthy
    └─ grafana:   http://localhost:3000/api/health
    │
    ▼
[status table / JSON] ─── stdout (唯一 JSON 对象) + stderr (__AR_PROGRESS__)
```

### 仓根结构

```
autoresearch/                  # repo root
├── README.md                  # D-01 极简宣言
├── AGENTS.md                  # D-02 仓约定（单源真相）
├── CLAUDE.md                  # D-02a symlink → AGENTS.md
├── LICENSE                    # MIT
├── .gitignore                 # Python / macOS / IDE / secrets
├── pyproject.toml             # uv/PEP 621
├── autoresearch/              # Python 包
│   ├── __init__.py
│   ├── __main__.py            # entry: python -m autoresearch
│   ├── cli.py                 # @click.group()
│   └── services/
│       ├── __init__.py
│       ├── _common.py         # health-check helpers (concurrent, requests)
│       ├── status.py
│       ├── start.py
│       └── stop.py
├── services/                  # 4 个服务 compose
│   ├── README.md
│   ├── archon/                # 只有 README（指 archon.diy）
│   ├── wandb/
│   │   ├── compose.yml
│   │   └── README.md
│   ├── prometheus/
│   │   ├── compose.yml
│   │   ├── prometheus.yml     # self-scrape config
│   │   └── README.md
│   └── grafana/
│       ├── compose.yml
│       ├── datasources.yml    # provisioning
│       └── README.md
├── tests/
│   ├── test_cli.py
│   ├── test_status.py
│   └── test_start_stop.py
└── diagram/                   # 已有；本阶段不动
    └── autoresearch_arch.svg
```

### Pattern 1: Click 树状子命令
**What:** `@click.group()` + `@group.command()` 嵌套
**When:** 8 个 skill 各自挂 group（Phase 1 只挂 services）
**Example:**
```python
# autoresearch/cli.py
import click

@click.group()
def main():
    """autoresearch — local LLM training workflow platform."""
    pass

@main.group()
def services():
    """Manage local dev services (Archon, wandb, Prometheus, Grafana)."""
    pass

@services.command(name="status")
@click.option("--json", "as_json", is_flag=True, help="Output machine-readable JSON.")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def status_cmd(as_json, lang):
    """Check health of all 4 services concurrently."""
    from .services.status import run
    run(as_json=as_json, lang=lang)
```

### Pattern 2: concurrent.futures 并发 healthz 探测
**What:** ThreadPoolExecutor 4 workers，每个 worker `requests.get(url, timeout=3)`
**When:** status 子命令固定 4 服务；顺序查询太慢
**Example:**
```python
# autoresearch/services/_common.py
from concurrent.futures import ThreadPoolExecutor
import requests

SERVICES = [
    ("archon",     "http://localhost:8088/healthz"),
    ("wandb",      "http://localhost:8080/healthz"),
    ("prometheus", "http://localhost:9090/-/healthy"),
    ("grafana",    "http://localhost:3000/api/health"),
]

def check_one(name: str, url: str, timeout: float = 3.0) -> dict:
    import time
    t0 = time.perf_counter()
    try:
        r = requests.get(url, timeout=timeout)
        latency_ms = int((time.perf_counter() - t0) * 1000)
        return {"name": name, "url": url, "healthy": r.ok,
                "latency_ms": latency_ms, "error": None}
    except Exception as e:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        return {"name": name, "url": url, "healthy": False,
                "latency_ms": latency_ms, "error": str(e)}

def check_all() -> list[dict]:
    with ThreadPoolExecutor(max_workers=len(SERVICES)) as ex:
        return list(ex.map(lambda s: check_one(*s), SERVICES))
```

### Pattern 3: Docker Compose 自监控 Prometheus
**What:** `prometheus.yml` scrape 它自己的 `/metrics` 端点
**When:** 启动 Prometheus 容器
**Example:**
```yaml
# services/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]
```

### Pattern 4: Grafana Provisioning Datasources
**What:** `datasources.yml` 在容器启动时由 Grafana 自动加载
**When:** 启动 Grafana 容器
**Example:**
```yaml
# services/grafana/datasources.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
  - name: wandb
    type: grafana-simple-json-datasource
    access: proxy
    url: http://host.docker.internal:8080
    isDefault: false
```

### Anti-Patterns to Avoid
- **直接用 `os.system("docker compose up")`：** 用 `subprocess.run(["docker", "compose", "-f", path, "up", "-d"], check=True)`，能捕获 exit code 和 stderr
- **同步顺序查 4 服务 healthz：** 慢；必须用 ThreadPoolExecutor
- **在 compose 里启 Archon：** 违反 D-05；Archon 是 `archon serve` 单独进程
- **把 README 写成长篇大论：** 违反 D-01；≤ 80 行
- **用 `os.path` 而非 `pathlib.Path`：** 现代 Python 用 pathlib
- **把 secrets 写进 compose：** 用 `.env.example` 占位 + 真实 `.env` 加进 .gitignore
</architecture_patterns>

<dont_hand_roll>
## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CLI 参数解析 | 手撸 argparse | `click` | 嵌套子命令 / 自动 help / 类型校验 click 都有 |
| HTTP health check | 手撸 socket | `requests.get(url, timeout=3)` | 错误处理、超时、SSL 全部白送 |
| 并发请求 | 手撸 threading | `concurrent.futures.ThreadPoolExecutor` | stdlib；4 worker 池足够；自动 shutdown |
| Docker Compose 启动 | 手撸 YAML 解析 | `subprocess.run(["docker", "compose", ...])` | 不重新发明 v2 plugin |
| YAML 加载（未来 Phase 2） | 手撸 split/join | `ruamel.yaml` | round-trip 保留注释 |
| 进度协议 | 手撸 print | `print("__AR_PROGRESS__=...", file=sys.stderr)` | Phase 2 才用；Phase 1 留好 `services/_progress.py` 接口 |
</dont_hand_roll>

<common_pitfalls>
## Common Pitfalls

### Pitfall 1: Mac 上 `host.docker.internal` 不通
**What goes wrong:** Grafana datasources.yml 里写 `http://localhost:8080`，Grafana 容器内 `localhost` 是容器自己，连不到 Mac 上的 wandb。
**Why it happens:** Docker Desktop for Mac 把容器放独立 VM；容器内 localhost ≠ Mac localhost。
**How to avoid:** 用 `host.docker.internal:8080`（Mac/Win 专属）；Linux 上需加 `extra_hosts: ["host.docker.internal:host-gateway"]`。
**Warning signs:** Grafana UI 里 datasource 标红 "Bad Gateway"。

### Pitfall 2: 端口被本机其他进程占用
**What goes wrong:** `docker compose up` 报 "bind: address already in use"。
**Why it happens:** Mac 上开发时可能 8080/9090/3000 被其他应用占。
**How to avoid:** README 明确端口冲突处理；`.env.example` 给端口变量；start 命令捕获错误并提示"端口 X 被占，请先释放"。
**Warning signs:** docker compose 退码 1，stderr 含 "bind"。

### Pitfall 3: Prometheus 容器内 scrape 自身失败
**What goes wrong:** `prometheus.yml` 写 `targets: ["localhost:9090"]`，但容器内 localhost 是容器自己，端口对、能 scrape；但如果写 `targets: ["prometheus:9090"]` 而服务名拼错，会连不上。
**How to avoid:** 容器内自监控就用 `localhost:9090`；跨容器才用服务名。
**Warning signs:** Prometheus UI 的 Status > Targets 页面里 job 显示 "down"。

### Pitfall 4: wandb local 镜像不带 /healthz
**What goes wrong:** `requests.get("http://localhost:8080/healthz")` 返回 404。
**Why it happens:** wandb local 镜像的 health 端点可能在 `/` 或 `/health` 而非 `/healthz`。
**How to avoid:** 实际验证 wandb local 的 health 端点；本 phase 在 RESEARCH 后用 `curl` 验证。**M1 假设 `/healthz`**（待 Plan 01-02 任务中验证）。
**Warning signs:** `services status` 显示 wandb 永远 unhealthy。

### Pitfall 5: Python 包名 `services` 跟 docker 子目录 `services/` 重名
**What goes wrong:** `from autoresearch.services import status` 与 `services/` 目录混淆。
**Why it happens:** Python 包结构与文件目录同名。
**How to avoid:** 包内用 `autoresearch/services/`（点号），文件目录用 `services/`（斜杠），互不干扰；通过 `__init__.py` 显式 import。
**Warning signs:** ImportError 报 "module 'autoresearch.services' has no attribute 'status'"。
</common_pitfalls>

<code_examples>
## Code Examples

### Example 1: cli.py 完整入口
```python
# autoresearch/cli.py
import click
from .services.status import run_status
from .services.start import run_start
from .services.stop import run_stop

@click.group()
@click.version_option()
def main():
    """autoresearch — local LLM training workflow platform."""
    pass

@main.group()
def services():
    """Manage local dev services (Archon, wandb, Prometheus, Grafana)."""
    pass

@services.command(name="status")
@click.option("--json", "as_json", is_flag=True, help="Output machine-readable JSON.")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def services_status(as_json: bool, lang: str):
    """Check health of all 4 local services concurrently."""
    run_status(as_json=as_json, lang=lang)

@services.command(name="start")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def services_start(lang: str):
    """Start 3 docker-compose services (wandb, prometheus, grafana). Archon is managed separately via `archon serve`."""
    run_start(lang=lang)

@services.command(name="stop")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def services_stop(lang: str):
    """Stop 3 docker-compose services."""
    run_stop(lang=lang)

if __name__ == "__main__":
    main()
```

### Example 2: status.py 完整实现
```python
# autoresearch/services/status.py
from __future__ import annotations
import json
import sys
from ._common import check_all, SERVICES

def run_status(*, as_json: bool, lang: str) -> int:
    results = check_all()
    if as_json:
        out = {
            "services": results,
            "summary": {
                "total": len(results),
                "healthy": sum(1 for r in results if r["healthy"]),
                "unhealthy": sum(1 for r in results if not r["healthy"]),
            },
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        # 人读表格
        hdr = f"{'NAME':<14}{'URL':<42}{'HEALTHY':<10}{'LATENCY_MS':<10}"
        print(hdr)
        for r in results:
            mark = "✓" if r["healthy"] else "✗"
            print(f"{r['name']:<14}{r['url']:<42}{mark:<10}{r['latency_ms']:<10}")
        n_h = sum(1 for r in results if r["healthy"])
        if lang == "zh":
            print(f"\n共 {len(results)} 服务，健康 {n_h}/{len(results)}", file=sys.stderr)
        else:
            print(f"\n{len(results)} services, {n_h}/{len(results)} healthy", file=sys.stderr)
    return 0 if all(r["healthy"] for r in results) else 1
```

### Example 3: start.py 串行调 compose
```python
# autoresearch/services/start.py
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPOSE_DIR = ROOT / "services"
# Archon 由 `archon serve` 管理；不列在这里
COMPOSE_SERVICES = ["wandb", "prometheus", "grafana"]

def _run_compose_up(svc: str) -> bool:
    compose_file = COMPOSE_DIR / svc / "compose.yml"
    print(f"[{svc}] docker compose -f {compose_file} up -d ...", file=sys.stderr)
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "-d"],
            check=False, capture_output=True, text=True,
        )
    except FileNotFoundError:
        print("错误：找不到 docker 命令。请先安装 Docker Desktop。", file=sys.stderr)
        return False
    if result.returncode != 0:
        print(f"[{svc}] FAILED: {result.stderr}", file=sys.stderr)
        return False
    print(f"[{svc}] OK", file=sys.stderr)
    return True

def run_start(*, lang: str) -> int:
    all_ok = True
    for svc in COMPOSE_SERVICES:
        if not _run_compose_up(svc):
            all_ok = False
            break  # 串行：失败则停
    if lang == "zh":
        print("Archon：由 `archon serve` 自行管理，不在 autoresearch 范围。", file=sys.stderr)
    else:
        print("Archon: managed by `archon serve`, not by autoresearch.", file=sys.stderr)
    return 0 if all_ok else 1
```

### Example 4: pyproject.toml 最小可用
```toml
# pyproject.toml
[project]
name = "autoresearch"
version = "0.1.0"
description = "Local LLM training workflow platform"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1",
    "requests>=2.31",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
]

[project.scripts]
autoresearch = "autoresearch.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["autoresearch"]
```

### Example 5: services/wandb/compose.yml
```yaml
# services/wandb/compose.yml
services:
  wandb:
    image: wandb/local:0.17.5
    container_name: ar-wandb
    ports:
      - "8080:8080"
    environment:
      - WANDB_BASE_URL=http://localhost:8080
    volumes:
      - wandb-data:/vol
    restart: unless-stopped

volumes:
  wandb-data:
```

### Example 6: services/prometheus/compose.yml
```yaml
# services/prometheus/compose.yml
services:
  prometheus:
    image: prom/prometheus:v2.51.0
    container_name: ar-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    command:
      - --config.file=/etc/prometheus/prometheus.yml
      - --storage.tsdb.path=/prometheus
    restart: unless-stopped
```

### Example 7: AGENTS.md 骨架
```markdown
# AGENTS.md — AutoResearch 仓协作者指南

## 仓约定
- **单源真相**：本文件即真相；`CLAUDE.md` 是相对路径 symlink
- **Python 3.11+**；包管理用 `uv`；CLI 框架用 `click`
- **服务编排**：每服务一个 `services/<name>/compose.yml`；串行 `up -d` 避免端口竞争
- **测试**：`pytest`；M1 阶段 01 可只做单测

## 8 步最小循环
| # | Skill | CLI group | Phase |
|---|-------|-----------|-------|
| 1 | customer-config | `autoresearch config` | 3 |
| 2 | local-services-health | `autoresearch services` | 1, 4 |
| 3 | server-hardware-probe | `autoresearch hw` | 5 |
| 4 | network-check | `autoresearch net` | 6 |
| 5 | service-reachability | `autoresearch reach` | 7 |
| 6 | train-stack-health | `autoresearch stack` | 8 |
| 7 | data-collection | `autoresearch collect` | 9 |
| 8 | experiment-report | `autoresearch report` | 10 |

## 三沉淀层
- `workspace-core/`：通用（SSH / config / secrets / progress / log / layout）
- `verl-workspace-adapter/`：训练栈适配
- `datalake/`：数据采集与持久化

## 进度协议
- 子命令最终 stdout 必须是**唯一一个** JSON 对象
- 过程进度走 stderr：`__AR_PROGRESS__=<json>`
- 模板（Phase 2 落 CORE-PROTO-01..02）

## 测试规范
- 单测放 `tests/`；命名 `test_<module>.py`
- M1 不强制覆盖率，但每个 CLI 子命令至少有 1 个 happy path 单测
```
</code_examples>

<sota_updates>
## State of Art (2026-06)

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `docker-compose` (v1 Python 工具) | `docker compose` (v2 Go plugin) | 2023 弃用 v1 | 2024 起 v2 是默认；必须用 `docker compose` 子命令 |
| 旧 `wandb/local` image | `wandb/local` 仍在维护；新版本偶尔改名 | 2024 | 仍可用 0.17.x；M1 锁 0.17.5 |
| 旧 `prom/prometheus` v2.40 | v2.51 LTS | 2024-12 | 自监控语法不变 |
| pip + requirements.txt | uv | 2024 起 | uv 速度优势明显；M1 直接采用 |
| 旧 `click` 7.x | 8.1.x | 2023 | 必须升级；decorator 行为更严格 |
| `print` 输出 | `__AR_PROGRESS__=` 协议 (vllm-ascend-workspace 模式) | 2024-2025 | AI 协作者友好；M1 留接口不强制 |

**新工具/模式可考虑：**
- `pydantic-settings` 配置文件加载（Phase 2 落 CORE-CFG）
- `rich` 美化 stdout（可选；M1 阶段不上）

**已弃用：**
- `docker-compose` v1 binary —— 完全弃用；v2 是子命令
- Python 3.9 及以下 —— 2025 起 EOL
</sota_updates>

<open_questions>
## Open Questions

1. **wandb local 的 health 端点是哪个？**
   - What we know: wandb/local 镜像的 `wandb` 进程监听 8080
   - What's unclear: `/healthz` vs `/health` vs `/` 的实际响应
   - Recommendation: Plan 01-02 任务中用 `curl http://localhost:8080/healthz` 验证；若 404，fallback 到 `/health`；在 `_common.py` 用常量配置

2. **Grafana 容器内 `host.docker.internal` 在 Linux 上需要额外配置吗？**
   - What we know: Mac/Windows 上 `host.docker.internal` 默认可用
   - What's unclear: 如果未来用户在 Linux 跑，是否需要 `extra_hosts: ["host.docker.internal:host-gateway"]`
   - Recommendation: M1 只面向 Mac（PROJECT.md 锁 Mac 单机）；Linux 支持留 Phase 2 之后

3. **uv 锁版本号？**
   - What we know: PROJECT.md 说"建议 uv，与现代 Python 栈一致"
   - What's unclear: 锁 `uv>=0.4` 还是不限
   - Recommendation: 锁 `>=0.4`；README 注明 "需先安装 uv"

4. **CLI 默认输出语言 — 全中文还是中英混排？**
   - What we know: D-04e 说最终 stdout 是唯一 JSON；M1 阶段 01-03 子命令可放宽为人读 + `--json` flag
   - What's unclear: 人读模式默认中文还是英文
   - Recommendation: 默认中文（中文用户群体）；`--lang en` 切英文（可选）
</open_questions>

<sources>
## Sources

### Primary (HIGH confidence)
- `.planning/PROJECT.md` — 哲学 / 锁定的技术栈 / 关键决策
- `.planning/ROADMAP.md` — Phase 1 目标 / 成功标准 / 3 个 plan 范围
- `.planning/phases/01-repo-foundation-services/01-CONTEXT.md` — D-01..D-06 锁定决策
- `.planning/REQUIREMENTS.md` — REPO-01..05, SVC-01..04
- `~/.codex/get-shit-done/templates/phase-prompt.md` — PLAN.md 格式
- `~/.codex/get-shit-done/references/planner-antipatterns.md` — 计划反模式
- Python click 8.1 官方文档 — @click.group / @group.command 模式
- Docker Compose v2 官方文档 — `docker compose -f <file> up -d` 用法
- Prometheus 官方文档 — 自监控 scrape config 语法
- Grafana 官方文档 — provisioning datasources 格式

### Secondary (MEDIUM confidence)
- vllm-ascend-workspace `__VAWS_REMOTE_TOOLBOX_PROGRESS__` 协议模式 — 进度协议参照

### Tertiary (LOW confidence - needs validation)
- wandb local 镜像的 `/healthz` 端点（需 Plan 01-02 任务中 curl 验证）
- Grafana `host.docker.internal` 在 Mac 上的可用性（依赖 Docker Desktop 版本）
</sources>

<metadata>
## Metadata

**Research scope:**
- Core technology: Python click + Docker Compose v2
- Ecosystem: click / requests / pytest / uv / Docker
- Patterns: CLI group tree / ThreadPoolExecutor / docker compose v2
- Pitfalls: host.docker.internal / 端口冲突 / Prometheus self-scrape / wandb healthz 端点

**Confidence breakdown:**
- Standard stack: HIGH — Python click / Docker Compose v2 / uv 全部行业标准
- Architecture: HIGH — D-01..D-06 锁定决策已经做了
- Pitfalls: MEDIUM — 已知 host.docker.internal 和端口问题；wandb healthz 端点需验证
- Code examples: HIGH — click / compose.yml 全部官方文档

**Research date:** 2026-06-06
**Valid until:** 2026-07-06 (30 天；Python click / Docker Compose v2 稳定)
</metadata>

---

*Phase: 01-repo-foundation-services*
*Research completed: 2026-06-06*
*Ready for planning: yes*
