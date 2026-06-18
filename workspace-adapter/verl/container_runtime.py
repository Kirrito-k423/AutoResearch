"""Runtime helpers for choosing between fresh docker runs and container reuse."""
from __future__ import annotations

import shlex
from pathlib import Path
from typing import Callable

from workspace_core.config import ServerSpec

from .docker import build_docker_exec_command


RemoteRunner = Callable[[ServerSpec, str, float], tuple[int, str, str]]

RESOURCE_BUSY_MARKERS = (
    "507899",
    "Resource_Busy",
    "aclInit",
    "rtGetDevMsg execution failed",
)


def is_resource_busy_error(text: str) -> bool:
    return any(marker in text for marker in RESOURCE_BUSY_MARKERS)


def discover_reusable_container(
    spec: ServerSpec,
    *,
    image: str,
    runner: RemoteRunner,
    timeout: float,
) -> tuple[str | None, str]:
    """Return a reusable container name when a compatible idle runtime exists."""
    query = (
        "docker ps --filter status=running "
        f"--filter ancestor={shlex.quote(image)} "
        "--format '{{.Names}}'"
    )
    code, stdout, stderr = runner(spec, query, min(timeout, 30.0))
    if code != 0:
        detail = (stderr or stdout or "").strip() or f"exit={code}"
        return None, f"query running containers failed: {detail}"

    names = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not names:
        return None, "no matching running container"
    if len(names) != 1:
        return None, f"ambiguous running containers: {', '.join(names)}"

    container_name = names[0]
    idle, idle_detail = _container_is_idle(
        spec,
        container_name=container_name,
        runner=runner,
        timeout=timeout,
    )
    if not idle:
        return None, idle_detail

    smoke_ok, smoke_detail = smoke_reusable_container(
        spec,
        container_name=container_name,
        runner=runner,
        timeout=timeout,
    )
    if not smoke_ok:
        return None, smoke_detail
    return container_name, smoke_detail


def smoke_reusable_container(
    spec: ServerSpec,
    *,
    container_name: str,
    runner: RemoteRunner,
    timeout: float,
) -> tuple[bool, str]:
    """Run a tiny torch_npu smoke test in an already-running container."""
    smoke = build_docker_exec_command(
        container_name=container_name,
        command="/bin/bash -lc "
        + shlex.quote(
            "python3 -c "
            "\"import torch, torch_npu; "
            "value = torch.tensor([1.0]).npu().tolist(); "
            "print('AR_FORMAL_SMOKE_OK=1'); "
            "print('AR_FORMAL_SMOKE_VALUE=' + repr(value))\""
        ),
    )
    code, stdout, stderr = runner(spec, smoke, min(timeout, 120.0))
    output = (stdout or "") + ("\n" + stderr if stderr else "")
    if code == 0 and "AR_FORMAL_SMOKE_OK=1" in output:
        return True, f"reused running container {container_name}"
    detail = output.strip().splitlines()[-1] if output.strip() else f"exit={code}"
    return False, f"reusable container smoke failed: {detail[:240]}"


def reusable_exec_paths(
    *,
    source_mounts: dict[str, str],
    remote_model_path: str | Path,
    remote_dataset_path: str | Path,
    remote_output_path: str | Path,
) -> dict[str, str]:
    """Translate staged host paths into in-container paths for docker exec mode."""
    paths = {
        "verl_root": source_mounts.get("/verl", "/verl"),
        "model_root": str(remote_model_path),
        "dataset_root": str(remote_dataset_path),
        "output_root": str(remote_output_path),
    }
    veomni_root = source_mounts.get("/veomni")
    if veomni_root:
        paths["veomni_root"] = veomni_root
    return paths


def _container_is_idle(
    spec: ServerSpec,
    *,
    container_name: str,
    runner: RemoteRunner,
    timeout: float,
) -> tuple[bool, str]:
    command = build_docker_exec_command(
        container_name=container_name,
        command="/bin/bash -lc "
        + shlex.quote(
            "ps -eo args= | grep -E "
            + shlex.quote(r"verl\.trainer\.main_ppo|VLLMWorker_TP|ray::|vllm")
            + " | grep -v grep || true"
        ),
    )
    code, stdout, stderr = runner(spec, command, min(timeout, 30.0))
    if code != 0:
        detail = (stderr or stdout or "").strip() or f"exit={code}"
        return False, f"failed to inspect reusable container activity: {detail}"
    active = [line.strip() for line in stdout.splitlines() if line.strip()]
    if active:
        return False, f"reusable container has active runtime processes: {active[0][:200]}"
    return True, f"reusable container {container_name} is idle"
