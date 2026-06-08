"""autoresearch CLI entry point."""
from __future__ import annotations

import click

from autoresearch import __version__


@click.group()
@click.version_option(__version__, prog_name="autoresearch")
def main() -> None:
    """autoresearch — local LLM training workflow platform.

    8 个 skill 串成最小循环 (customer-config → local-services-health → ...)，
    单二进制入口；每个 skill 挂一个 group。
    """
    pass


@main.group()
def services() -> None:
    """管理本地开发服务（Archon、wandb、Prometheus、Grafana）。"""
    pass


@services.command(name="status")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output machine-readable JSON.",
)
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en)。",
)
def services_status(as_json: bool, lang: str) -> None:
    """并发查询 4 个服务的 /healthz 端点。"""
    from autoresearch.services.status import run_status
    raise click.exceptions.Exit(run_status(as_json=as_json, lang=lang))


@services.command(name="start")
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en)。",
)
def services_start(lang: str) -> None:
    """启动 3 个 docker-compose 服务（wandb/prometheus/grafana）。

    Archon 由 `archon serve` 自行管理，不在 autoresearch 范围（D-05）。
    """
    from autoresearch.services.start import run_start
    raise click.exceptions.Exit(run_start(lang=lang))


@services.command(name="stop")
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en)。",
)
def services_stop(lang: str) -> None:
    """停止 3 个 docker-compose 服务。"""
    from autoresearch.services.stop import run_stop
    raise click.exceptions.Exit(run_stop(lang=lang))


@main.command()
@click.option(
    "--server",
    default=None,
    help="server alias (走 config/config.yaml); 不传走 dummy server。",
)
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en).",
)
def ping(server: str | None, lang: str) -> None:
    """SSH 端到端冒烟: echo ok + 反向代理通断 (D-18, D-19, D-20).

    默认走 paramiko dummy server (无外部依赖). 传 --server <alias> 走真 SSH.
    """
    from autoresearch.ping import run_ping
    raise click.exceptions.Exit(run_ping(server=server, lang=lang))


# === Phase 3 / Skill 01: customer-config ===

@main.group()
def config() -> None:
    """管理配置: 模板生成 / 校验 / 脱敏查看 (Skill 01)."""
    pass


@config.command(name="init")
@click.option("--force", is_flag=True, help="覆盖现有 config/config.yaml.")
@click.option("--config", "cfg_path", default=None, help="写到指定路径 (默认 ./config/config.yaml).")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_init(force: bool, cfg_path: str | None, lang: str) -> None:
    """生成 config/config.yaml 模板 (复制 config.example.yaml)."""
    from autoresearch.config import run_init
    raise click.exceptions.Exit(run_init(force=force, config=cfg_path, lang=lang))


@config.command(name="validate")
@click.option("--config", "cfg_path", default=None, help="校验指定文件 (默认 ./config/config.yaml).")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出.")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_validate(cfg_path: str | None, as_json: bool, lang: str) -> None:
    """校验现有 config 走 Pydantic + 中文错误."""
    from autoresearch.config import run_validate
    raise click.exceptions.Exit(run_validate(config=cfg_path, lang=lang, as_json=as_json))


@config.command(name="show")
@click.option("--config", "cfg_path", default=None, help="查看指定文件 (默认 ./config/config.yaml).")
@click.option("--json", "as_json", is_flag=True, help="JSON 输出 (敏感字段已脱敏).")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_show(cfg_path: str | None, as_json: bool, lang: str) -> None:
    """打印配置, 敏感字段显示为 *** (CFG-SHOW-01)."""
    from autoresearch.config import run_show
    raise click.exceptions.Exit(run_show(config=cfg_path, lang=lang, as_json=as_json))


# === Phase 3 / Skill 01: keyring sub-group ===

@config.group()
def keyring_grp() -> None:
    """macOS Keychain / 系统 keyring 集成 (D-05)."""
    pass


@keyring_grp.command(name="set")
@click.argument("name")
@click.option("--value", required=True, help="要存的密码值.")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_keyring_set(name: str, value: str, lang: str) -> None:
    """存密码到 keyring: autoresearch/<name>."""
    from autoresearch.config import run_keyring
    raise click.exceptions.Exit(run_keyring(action="set", name=name, value=value, lang=lang))


@keyring_grp.command(name="get")
@click.argument("name")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_keyring_get(name: str, lang: str) -> None:
    """从 keyring 读密码: autoresearch/<name>."""
    from autoresearch.config import run_keyring
    raise click.exceptions.Exit(run_keyring(action="get", name=name, lang=lang))


@keyring_grp.command(name="delete")
@click.argument("name")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_keyring_delete(name: str, lang: str) -> None:
    """从 keyring 删密码."""
    from autoresearch.config import run_keyring
    raise click.exceptions.Exit(run_keyring(action="delete", name=name, lang=lang))


@keyring_grp.command(name="list")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def config_keyring_list(lang: str) -> None:
    """提示 keyring 无原生 list API (Phase 2 D-09 已说明)."""
    from autoresearch.config import run_keyring
    raise click.exceptions.Exit(run_keyring(action="list", name="", lang=lang))


if __name__ == "__main__":
    main()
