"""autoresearch CLI entry point."""
from __future__ import annotations

import click
import sys
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


# === Phase 4 / Skill 03: server-hardware-probe ===

@main.group()
def hw() -> None:
    """探测远程 Ascend 服务器硬件。"""
    pass


@hw.command(name="probe")
@click.option(
    "--server",
    default=None,
    help="config 中的服务器名称。",
)
@click.option(
    "--all",
    "all_servers",
    is_flag=True,
    help="探测 config 中的全部服务器（最多 3 个并发）。",
)
@click.option(
    "--config",
    "cfg_path",
    default=None,
    help="配置文件路径 (默认 ./config/config.yaml)。",
)
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en)。",
)
def hw_probe(
    server: str | None,
    all_servers: bool,
    cfg_path: str | None,
    lang: str,
) -> None:
    """通过 SSH 执行 npu-smi 并输出核心 NPU 指标 JSON。"""
    from autoresearch.hw.probe import run_probe
    raise click.exceptions.Exit(
        run_probe(
            server=server,
            all_servers=all_servers,
            config=cfg_path,
            lang=lang,
        )
    )


# === Phase 5 / Skill 04: network-check ===

@main.group()
def net() -> None:
    """探测本机与远程服务器外网可达性。"""
    pass


@net.command(name="probe")
@click.option(
    "--server",
    default=None,
    help="只探测指定 config 服务器；不传则探测全部服务器。",
)
@click.option(
    "--local-only",
    is_flag=True,
    help="只探测本机网络，不连接远程服务器。",
)
@click.option(
    "--config",
    "cfg_path",
    default=None,
    help="配置文件路径 (默认 ./config/config.yaml)。",
)
@click.option(
    "--local-proxy-url",
    default="http://127.0.0.1:7890",
    help="本机代理地址，用于 huggingface/github fallback。",
)
@click.option(
    "--remote-proxy-port",
    default=17890,
    type=int,
    help="远程 ssh -R 代理端口。",
)
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en)。",
)
def net_probe(
    server: str | None,
    local_only: bool,
    cfg_path: str | None,
    local_proxy_url: str,
    remote_proxy_port: int,
    lang: str,
) -> None:
    """输出本机 + 远程网络测速矩阵 JSON。"""
    from autoresearch.net.probe import run_probe

    raise click.exceptions.Exit(
        run_probe(
            server=server,
            local_only=local_only,
            config=cfg_path,
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
            lang=lang,
        )
    )


@net.group(name="tunnel")
def net_tunnel() -> None:
    """管理远程反向代理隧道。"""
    pass


@net_tunnel.command(name="ensure")
@click.option(
    "--server",
    required=True,
    help="config 中的服务器名称。",
)
@click.option(
    "--config",
    "cfg_path",
    default=None,
    help="配置文件路径 (默认 ./config/config.yaml)。",
)
@click.option(
    "--local-proxy-url",
    default="http://127.0.0.1:7890",
    help="本机代理地址。",
)
@click.option(
    "--remote-proxy-port",
    default=17890,
    type=int,
    help="远程 ssh -R 代理端口。",
)
@click.option(
    "--lang",
    default="zh",
    type=click.Choice(["zh", "en"]),
    help="输出语言 (zh/en)。",
)
def net_tunnel_ensure(
    server: str,
    cfg_path: str | None,
    local_proxy_url: str,
    remote_proxy_port: int,
    lang: str,
) -> None:
    """确保指定服务器上的反向代理隧道可用。"""
    from autoresearch.net.tunnel import run_tunnel_ensure

    raise click.exceptions.Exit(
        run_tunnel_ensure(
            server=server,
            config=cfg_path,
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
            lang=lang,
        )
    )


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


@main.group(name="collect")
def collect() -> None:
    """数据采集: minimal run + wandb/log/prom/manifest."""
    pass


from autoresearch.collect.cli import run as collect_run_command

collect.add_command(collect_run_command)


@main.group(name="report")
def report() -> None:
    """实验报告: 读取本地 run artifact 生成单页 HTML。"""
    pass


from autoresearch.report.cli import render as report_render_command

report.add_command(report_render_command)


if __name__ == "__main__":
    main()


# === Phase 4.x / BMC: 带外管理 (Redfish) ===

@main.group()
def bmc() -> None:
    """带外管理 (BMC) skill — Redfish 协议 (iBMC 等).

    安全门 (D-32):
      - power off/on/cycle 默认 DRY-RUN, 只打印意图
      - --apply 才真正下发 BMC Reset
      - config bmc.power_operations_allowed=false 时, --apply 一定拒绝
    """
    pass


def _resolve_bmc(server: str, cfg_path: str | None) -> tuple[str, Any]:
    """helper: 从 config 找 server 并取 bmc 段."""
    from workspace_core.config import from_path, ConfigError
    cfg = from_path(cfg_path)
    spec = next((s for s in cfg.servers if s.name == server), None)
    if spec is None:
        available = [s.name for s in cfg.servers]
        raise ConfigError(
            f"config.servers 中找不到 '{server}'; 已配: {available}"
        )
    if spec.bmc is None:
        raise ConfigError(
            f"server '{server}' 未配置 bmc 段 (servers[].bmc=null)"
        )
    return server, spec.bmc


@bmc.command(name="identify")
@click.option("--server", required=True, help="config 中的服务器名.")
@click.option("--config", "cfg_path", default=None, help="配置文件路径.")
@click.option(
    "--verify-ssl",
    is_flag=True,
    help="校验 BMC SSL 证书 (内网 BMC 一般自签, 默认不校验).",
)
def bmc_identify(server: str, cfg_path: str | None, verify_ssl: bool) -> None:
    """通过 Redfish 拉机器唯一硬件编码 (BMC UUID / System SerialNumber / SKU)."""
    import json as _json
    from workspace_core.config import ConfigError
    from autoresearch.bmc import identify_server
    try:
        _, bmc_spec = _resolve_bmc(server, cfg_path)
    except ConfigError as exc:
        print(f"配置错误: {exc}", file=sys.stderr)
        print(_json.dumps(
            {"ok": False, "severity": "fail", "data": {}, "message": "配置错误", "error": str(exc)},
            ensure_ascii=False,
        ))
        raise click.exceptions.Exit(2)
    result = identify_server(bmc_spec, verify_ssl=verify_ssl)
    if result["error"]:
        print(f"{result['message']}: {result['error']}", file=sys.stderr)
    print(_json.dumps(result, ensure_ascii=False))
    raise click.exceptions.Exit(0 if result["ok"] else 1)


@bmc.group()
def power() -> None:
    """电源操作: status / off / on / cycle. 默认 DRY-RUN."""
    pass


def _run_power(op: str, server: str, cfg_path: str | None, apply: bool, verify_ssl: bool) -> None:
    import json as _json
    from workspace_core.config import ConfigError
    from autoresearch.bmc import power_status, power_off, power_on, power_cycle
    try:
        _, bmc_spec = _resolve_bmc(server, cfg_path)
    except ConfigError as exc:
        print(f"配置错误: {exc}", file=sys.stderr)
        print(_json.dumps(
            {"ok": False, "severity": "fail", "data": {}, "message": "配置错误", "error": str(exc)},
            ensure_ascii=False,
        ))
        raise click.exceptions.Exit(2)
    fn = {
        "status": power_status,
        "off": power_off,
        "on": power_on,
        "cycle": power_cycle,
    }[op]
    result = fn(bmc_spec, apply=apply, verify_ssl=verify_ssl)
    if result["error"]:
        print(f"{result['message']}: {result['error']}", file=sys.stderr)
    print(_json.dumps(result, ensure_ascii=False))
    raise click.exceptions.Exit(0 if result["ok"] else 1)


@power.command(name="status")
@click.option("--server", required=True)
@click.option("--config", "cfg_path", default=None)
@click.option("--verify-ssl", is_flag=True)
def bmc_power_status(server: str, cfg_path: str | None, verify_ssl: bool) -> None:
    """读 BMC 电源状态 (无破坏性, 不需要 --apply)."""
    _run_power("status", server, cfg_path, apply=False, verify_ssl=verify_ssl)


@power.command(name="off")
@click.option("--server", required=True)
@click.option("--config", "cfg_path", default=None)
@click.option("--apply", is_flag=True, help="真正下发 ResetType=ForceOff. 默认 dry-run.")
@click.option("--verify-ssl", is_flag=True)
def bmc_power_off(server: str, cfg_path: str | None, apply: bool, verify_ssl: bool) -> None:
    """强制下电 (ForceOff). 默认 DRY-RUN."""
    _run_power("off", server, cfg_path, apply=apply, verify_ssl=verify_ssl)


@power.command(name="on")
@click.option("--server", required=True)
@click.option("--config", "cfg_path", default=None)
@click.option("--apply", is_flag=True)
@click.option("--verify-ssl", is_flag=True)
def bmc_power_on(server: str, cfg_path: str | None, apply: bool, verify_ssl: bool) -> None:
    """上电 (On). 默认 DRY-RUN."""
    _run_power("on", server, cfg_path, apply=apply, verify_ssl=verify_ssl)


@power.command(name="cycle")
@click.option("--server", required=True)
@click.option("--config", "cfg_path", default=None)
@click.option("--apply", is_flag=True)
@click.option("--verify-ssl", is_flag=True)
def bmc_power_cycle(server: str, cfg_path: str | None, apply: bool, verify_ssl: bool) -> None:
    """强制下电 + 上电 (PowerCycle). 默认 DRY-RUN."""
    _run_power("cycle", server, cfg_path, apply=apply, verify_ssl=verify_ssl)


# === Phase 4.x / SSH bootstrap: key 部署 + NOPASSWD sudo 安装 (D-34) ===

@main.group()
def ssh() -> None:
    """SSH 远端服务器 bootstrap 工具 (key 部署 + NOPASSWD sudo 安装).

    所有写操作默认 dry-run, 须 --apply 才执行.
    """
    pass


def _print_result(result) -> None:
    """统一 CheckResult -> 单 JSON + 错误 stderr."""
    import json as _json
    if result["error"]:
        print(f"{result['message']}: {result['error']}", file=sys.stderr)
    print(_json.dumps(result, ensure_ascii=False))


@ssh.command(name="status")
@click.option("--server", default=None, help="指定一台; 不传看全部.")
@click.option("--config", "cfg_path", default=None, help="配置文件路径.")
def ssh_status(server: str | None, cfg_path: str | None) -> None:
    """检查每台 server 的 key 部署 + NOPASSWD sudo 状态."""
    from autoresearch.ssh_bootstrap import run_ssh_status
    result = run_ssh_status(server_name=server, config_path=cfg_path)
    _print_result(result)
    raise click.exceptions.Exit(0 if result["ok"] else 1)


@ssh.command(name="deploy-key")
@click.option("--server", required=True, help="config 中的服务器名.")
@click.option("--config", "cfg_path", default=None, help="配置文件路径.")
@click.option("--apply", is_flag=True, help="真正写远端; 默认 dry-run.")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def ssh_deploy_key(server: str, cfg_path: str | None, apply: bool, lang: str) -> None:
    """把本机 ~/.ssh/id_ed25519.pub 追加到远端 <user>/.ssh/authorized_keys.

    流程: 1) ensure_local_keypair 2) SSH 密码认证 (force_password)
    3) 追加公钥 (已存在则跳过) 4) chmod 600 5) 写本地 marker
    6) 第二次 connect 走 key 验证
    """
    from autoresearch.ssh_bootstrap import run_deploy_key
    result = run_deploy_key(server, config_path=cfg_path, apply=apply, lang=lang)
    _print_result(result)
    raise click.exceptions.Exit(0 if result["ok"] else 1)


@ssh.command(name="install-nopasswd-sudo")
@click.option("--server", required=True, help="config 中的服务器名.")
@click.option("--config", "cfg_path", default=None, help="配置文件路径.")
@click.option("--apply", is_flag=True, help="真正写远端 /etc/sudoers.d; 默认 dry-run.")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def ssh_install_nopasswd_sudo(server: str, cfg_path: str | None, apply: bool, lang: str) -> None:
    """给 <user> 装 NOPASSWD sudo 规则 (写到 /etc/sudoers.d/<user>-nopasswd).

    流程: 1) 备份 /etc/sudoers 2) 写 /etc/sudoers.d/<user>-nopasswd
    3) visudo -c 校验 (失败回滚) 4) sudo -n whoami 验证
    """
    from autoresearch.ssh_bootstrap import run_install_nopasswd_sudo
    result = run_install_nopasswd_sudo(server, config_path=cfg_path, apply=apply, lang=lang)
    _print_result(result)
    raise click.exceptions.Exit(0 if result["ok"] else 1)


@main.group(name="reach")
def reach() -> None:
    """远程服务可达性测试 (Phase 06): wandb + pushgateway."""
    pass


@reach.command(name="test")
@click.option("--server", default=None, help="config 中的服务器名称 (与 --all 互斥).")
@click.option("--all", "all_servers", is_flag=True, help="并发探测全部 config 中的服务器 (最多 3 worker).")
@click.option("--config", "cfg_path", default=None, help="配置文件路径 (默认 ./config/config.yaml).")
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def reach_test(
    server: str | None,
    all_servers: bool,
    cfg_path: str | None,
    lang: str,
) -> None:
    """验证指定服务器能通过 SSH 反向代理隧道访问本地 wandb (8080) + pushgateway (9091).

    --server X 单机; --all 并发跑全部. 走 net tunnel ensure 17890 验 wandb /healthz;
    临时建 17891 推 pushgateway metric.
    """
    if (server is None) == (not all_servers):
        # 既不传 --server 也不传 --all, 或两者都传了
        click.echo("错误: --server X 与 --all 必须二选一", err=True)
        raise click.exceptions.Exit(2)
    from autoresearch.reach.tester import run_reach_test, run_reach_test_all
    if all_servers:
        exit_code = run_reach_test_all(config=cfg_path, lang=lang)
    else:
        assert server is not None
        exit_code = run_reach_test(server=server, config=cfg_path, lang=lang)
    raise click.exceptions.Exit(exit_code)


@main.group(name="stack")
def stack() -> None:
    """远程训练栈健康检查 (Phase 07): conda env + verl/veomni import + NPU 1-step 干跑."""
    pass


@stack.command(name="check")
@click.option("--server", default=None, help="config 中的服务器名称 (与 --all 互斥).")
@click.option("--all", "all_servers", is_flag=True, help="并发探测全部 config 中的服务器 (最多 3 worker).")
@click.option("--config", "cfg_path", default=None, help="配置文件路径 (默认 ./config/config.yaml).")
@click.option(
    "--lib",
    "libs",
    multiple=True,
    help="要检测的库, 多次传叠加 (默认 verl + veomni).",
)
@click.option("--lang", default="zh", type=click.Choice(["zh", "en"]))
def stack_check(
    server: str | None,
    all_servers: bool,
    cfg_path: str | None,
    libs: tuple[str, ...],
    lang: str,
) -> None:
    """验证指定服务器 verl/veomni 训练栈就绪 (conda env + import + 1-step NPU 干跑).

    --server X 单机; --all 并发跑全部. 走 `conda run -n <env>` 验库 + 1-step 干跑.
    """
    if (server is None) == (not all_servers):
        click.echo("错误: --server X 与 --all 必须二选一", err=True)
        raise click.exceptions.Exit(2)
    from autoresearch.stack.checker import run_stack_check, run_stack_check_all
    lib_tuple = tuple(libs) if libs else None
    if all_servers:
        exit_code = run_stack_check_all(config=cfg_path, libs=lib_tuple, lang=lang)
    else:
        assert server is not None
        exit_code = run_stack_check(server=server, config=cfg_path, libs=lib_tuple, lang=lang)
    raise click.exceptions.Exit(exit_code)
