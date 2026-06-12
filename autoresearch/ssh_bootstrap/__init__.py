"""autoresearch.ssh_bootstrap — 一键把远端 server 配成"key + NOPASSWD sudo"状态.

三类子命令 (CLI):
  - deploy-key: 把本机 ~/.ssh/id_ed25519.pub 部署到远端 <user> 的 authorized_keys
  - install-nopasswd-sudo: 给 <user> 装 NOPASSWD sudo 规则 (写 /etc/sudoers.d/)
  - status: 检查每台 server 的 key 部署 + sudo 状态

设计 (D-34):
- 全部 --apply 默认 dry-run (只打印意图, 不动远端)
- 写 authorized_keys 用追加 (不覆盖)
- 写 sudoers.d/<name> 而不是直接改 sudoers; 写完 visudo -c 校验
- 每步出错立即回滚 (删追加的 key 行 / rm sudoers.d 文件)
"""
from .deploy import run_deploy_key
from .sudo import run_install_nopasswd_sudo
from .status import run_ssh_status

__all__ = [
    "run_deploy_key",
    "run_install_nopasswd_sudo",
    "run_ssh_status",
]
