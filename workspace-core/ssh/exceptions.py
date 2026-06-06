"""SSH 相关异常层级 (D-01 抹平). 所有异常继承 SSHError 基类."""
from __future__ import annotations


class SSHError(Exception):
    """SSH 操作基类错误. message 包含主机名 + 阶段 + 原因."""


class HostResolveError(SSHError):
    """~/.ssh/config alias 解析失败 / 直接形式语法错."""


class ConnectError(SSHError):
    """网络层连接失败 (timeout / DNS / refused). 重试有意义."""


class AuthError(SSHError):
    """认证失败. 重试无意义, 需用户介入."""


class BootstrapFailed(SSHError):
    """Bootstrap 阶段: 密码登录成功但部署公钥失败."""


class KeyDeployError(SSHError):
    """公钥部署 sftp 写失败 (权限 / 空间)."""


class TunnelError(SSHError):
    """反向代理 ssh -R 启动失败."""
