# Archon (本目录为占位说明)

> **Archon 不在 autoresearch 的 docker-compose 里**（D-05 锁定决策）。
> 本目录存在仅为标记服务位置 + 文档化外部安装步骤。

## 为什么不在 compose 里

Archon 是 MIT 工作流编排器（[coleam00/Archon](https://github.com/coleam00/Archon)），有自己的 CLI 工具链。
把它塞进我们的 compose 会导致：
- 与我们 8 skill 边界混乱（Archon 期望自家工作流 YAML）
- 镜像版本/升级节奏与我们的需求脱节
- 跨机器迁移时 Archon 配置丢失风险

## 安装 Archon（前置条件）

Archon 不在我们的 `docker-compose.yml` 里，由用户自行安装：

```bash
# macOS
brew install archon

# 或从源码
git clone https://github.com/coleam00/Archon.git
cd Archon
pip install -e .
```

详见官方安装指南：https://archon.diy/

## 启动 Archon

```bash
archon serve &     # 默认监听 :8088
# 或前台运行（看 log 方便调试）
archon serve
```

启动后验证：
```bash
curl http://localhost:8088/healthz
# 期望返回 200 OK
```

## autoresearch 与 Archon 的关系

- `autoresearch services status` **会**检查 Archon 的 `/healthz`（端口 8088）
- `autoresearch services start` **不会**启 Archon；只会起 wandb / prometheus / grafana 3 个
- Archon 安装是进入 Phase 1 之前的**前置条件**（README.md quickstart 写明）

## 故障排查

| 现象 | 原因 | 修复 |
|------|------|------|
| `archon: command not found` | 未安装 | 按上面"安装 Archon"步骤操作 |
| `/healthz` 404 | Archon 启动失败 | 看 `archon serve` 的 stderr；常见是端口 8088 被占 |
| 端口 8088 被占 | 其他应用占 | `lsof -i :8088` 找占端口进程；或改 Archon 端口 + `services/_common.py` 同步 |
