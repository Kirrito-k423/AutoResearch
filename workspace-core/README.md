# workspace-core — 沉淀 1：通用底座

> 8 skill 共用的通用工具。**不依赖** workspace-adapter 或 datalake。

## 职责

提供所有 skill 都可能用到的基础能力：

| 子模块 | 职责 | 关键接口 |
|---|---|---|
| `ssh/` | paramiko SSH 客户端 + 反向代理 | `SSHClient.connect()`, `ReverseTunnel.open()` |
| `secrets/` | 凭据加密、keyring | `KeyringBackend.get/set` |
| `config/` | Pydantic 加载/校验 | `Config.from_yaml(path)` |
| `progress/` | `__AR_PROGRESS__=<json>` 协议 | `emit_progress(stage, **fields)` |
| `result/` | CheckResult schema (ok/warn/fail + data) | `CheckResult(ok, data, message)` |
| `layout/` | 固定目录约定 `~/.autoresearch/{runs,logs,cache}/` | `Layout.ensure()` |
| `log/` | 统一日志格式 (人类 + JSON) | `get_logger(name)` |

## 设计原则

- **零状态**：所有模块 stateless；状态由 skill 自己写到 `~/.autoresearch/`
- **零网络**：本层不直接发网络请求（HTTP 客户端由调用方选择）
- **零训练栈概念**：本层**不知道** verl/veomni/npu-smi 是什么

## 状态

⏳ **Phase 2 待开发** — 当前目录为占位（结构可见 / 用途明确）。

---
*详细设计见 `.planning/phases/02-workspace-core/02-CONTEXT.md`（phase 2 计划时建）*
