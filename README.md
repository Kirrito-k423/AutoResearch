# AutoResearch

> 本地驱动的 LLM 训练/调试工作流平台。所有数据留在本机 Mac；远程 NPU 服务器只是被远控的执行终端。

## 核心价值

"常实践，详记录，知得失，会设计，有整理" —— 每个 skill 跑一次都留下可被复盘、可被二次开发的产物。

## 快速开始

```bash
git clone https://github.com/<org>/autoresearch.git
cd autoresearch
# 1) 装 Archon CLI（前置条件；详见 services/archon/README.md）
brew install archon   # 或见 archon.diy
archon serve &        # 启动 Archon（用户自行管理）
# 2) 启本地服务栈
autoresearch services start
# 3) 验证全绿
autoresearch services status
```

## 架构

4 列架构图见 [diagram/autoresearch_arch.svg](diagram/autoresearch_arch.svg)。

## 8 步最小循环

详细描述见 [.planning/ROADMAP.md](.planning/ROADMAP.md)。概览：customer-config → local-services-health → server-hardware-probe → network-check → service-reachability → train-stack-health → data-collection → experiment-report。

## 文档

- [AGENTS.md](AGENTS.md) — AI 协作者指南（必读）
- [.planning/PROJECT.md](.planning/PROJECT.md) — 项目哲学 / 约束 / 关键决策
- [.planning/ROADMAP.md](.planning/ROADMAP.md) — 14 阶段路线图

## License

[MIT](LICENSE)
