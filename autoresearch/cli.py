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


if __name__ == "__main__":
    main()
