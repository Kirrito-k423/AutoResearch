"""Docker command builders for Ascend Verl formal cases."""
from __future__ import annotations

import shlex
from pathlib import Path


ASCEND_CONTROL_DEVICES = (
    "/dev/davinci_manager",
    "/dev/devmm_svm",
    "/dev/hisi_hdc",
)

ASCEND_DRIVER_MOUNTS = (
    ("/usr/local/Ascend/driver/lib64", "/usr/local/Ascend/driver/lib64"),
    ("/usr/local/Ascend/driver/tools", "/usr/local/Ascend/driver/tools"),
    ("/usr/local/Ascend/add-ons", "/usr/local/Ascend/add-ons"),
)


def _q(value: str | Path) -> str:
    return shlex.quote(str(value))


def build_docker_pull_command(image: str, proxy_url: str | None = None) -> str:
    """Build a docker pull command for the selected Verl image."""
    parts: list[str] = []
    if proxy_url:
        parts.extend(
            [
                "env",
                f"http_proxy={_q(proxy_url)}",
                f"https_proxy={_q(proxy_url)}",
                f"HTTP_PROXY={_q(proxy_url)}",
                f"HTTPS_PROXY={_q(proxy_url)}",
                f"all_proxy={_q(proxy_url)}",
                f"ALL_PROXY={_q(proxy_url)}",
                "no_proxy=localhost,127.0.0.1,.huawei.com",
                "NO_PROXY=localhost,127.0.0.1,.huawei.com",
            ]
        )
    parts.extend(["docker", "pull", _q(image)])
    return " ".join(parts)


def build_docker_run_command(
    *,
    image: str,
    run_id: str,
    model_mount: str | Path,
    dataset_mount: str | Path,
    output_mount: str | Path,
    source_mounts: dict[str, str | Path] | None = None,
    command: str = "/bin/bash",
    proxy_url: str | None = None,
    shm_size: str = "64G",
    container_name: str | None = None,
    device_count: int = 8,
    network_host: bool = True,
) -> str:
    """Build an Ascend A2 compatible docker run command.

    The shape follows the VeOmni Ascend Docker guide while keeping host paths
    shell-quoted and all mounts explicit.
    """
    name = container_name or f"autoresearch-verl-{run_id}"
    parts = [
        "docker",
        "run",
        "--rm",
        "--runtime=runc",
        "-i",
        "--ulimit",
        "nproc=65535",
        "--ulimit",
        "nofile=65535",
    ]
    for device in _davinci_devices(device_count) + ASCEND_CONTROL_DEVICES:
        parts.append(f"--device={device}")
    if network_host:
        parts.append("--network=host")
    parts.append(f"--shm-size={shm_size}")
    for host_path, container_path in ASCEND_DRIVER_MOUNTS:
        parts.extend(["-v", f"{_q(host_path)}:{_q(container_path)}:ro"])
    parts.extend(
        [
            "-v",
            f"{_q(model_mount)}:/app/ckpt:ro",
            "-v",
            f"{_q(dataset_mount)}:/app/dataset:ro",
            "-v",
            f"{_q(output_mount)}:/app/output",
        ]
    )
    for container_path, host_path in (source_mounts or {}).items():
        parts.extend(["-v", f"{_q(host_path)}:{_q(container_path)}"])
    if proxy_url:
        for key in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
            parts.extend(["-e", f"{key}={_q(proxy_url)}"])
        for key in ("no_proxy", "NO_PROXY"):
            parts.extend(["-e", f"{key}=localhost,127.0.0.1,.huawei.com"])
    parts.extend(["--name", _q(name), _q(image), command])
    return " ".join(parts)


def _davinci_devices(device_count: int) -> tuple[str, ...]:
    if device_count < 1:
        raise ValueError("device_count must be >= 1")
    return tuple(f"/dev/davinci{index}" for index in range(device_count))
