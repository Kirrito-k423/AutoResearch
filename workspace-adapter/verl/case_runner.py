"""Remote formal Verl case runner."""
from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field

from workspace_core.config import ServerSpec

from ..common.conda_utils import run_in_env
from .case_config import (
    VerlCaseResultRow,
    VerlCaseRunConfig,
)
from .docker import build_docker_pull_command, build_docker_run_command


RemoteRunner = Callable[[ServerSpec, str, float], tuple[int, str, str]]


class VerlCaseRunResult(BaseModel):
    """Top-level formal case runner result."""

    ok: bool
    run_id: str
    rows: list[VerlCaseResultRow] = Field(default_factory=list)
    commands: list[str] = Field(default_factory=list)
    remote_matrix_path: str | None = None
    remote_log_path: str | None = None
    error: str | None = None


def _default_runner(spec: ServerSpec, command: str, timeout: float) -> tuple[int, str, str]:
    return run_in_env(spec, command, conda_env=getattr(spec, "conda_env", "") or "", workdir=getattr(spec, "workdir", "") or "", timeout=timeout)


def build_remote_case_script(run_config: VerlCaseRunConfig) -> str:
    """Render the remote script payload. Tests assert critical config values."""
    payload = run_config.model_dump(mode="json")
    return (
        "#!/usr/bin/env python3\n"
        "import json\n"
        f"RUN_CONFIG = {json.dumps(payload, ensure_ascii=False)}\n"
        "assert RUN_CONFIG['config']['ignore_eos'] is False\n"
        "print(json.dumps({'status': 'ready', 'ignore_eos': False}))\n"
    )


def run_verl_case(
    spec: ServerSpec,
    run_config: VerlCaseRunConfig,
    *,
    timeout: float,
    proxy_url: str | None = None,
    remote_model_path: str | Path = "/home/t00906153/autoresearch/model",
    remote_dataset_path: str | Path = "/home/t00906153/autoresearch/dataset",
    remote_output_path: str | Path | None = None,
    runner: RemoteRunner = _default_runner,
) -> VerlCaseRunResult:
    """Run every strict matrix row on the remote host via Docker."""
    output_path = Path(remote_output_path or f"/home/t00906153/autoresearch/runs/{run_config.run_id}")
    commands: list[str] = []
    rows: list[VerlCaseResultRow] = []
    pull = build_docker_pull_command(run_config.config.docker_image)
    commands.append(pull)
    pull_code, pull_stdout, pull_stderr = runner(spec, pull, timeout)
    if pull_code != 0:
        return VerlCaseRunResult(
            ok=False,
            run_id=run_config.run_id,
            commands=commands,
            rows=[],
            error=pull_stderr or pull_stdout or "docker pull failed",
        )

    remote_log_path = str(output_path / "verl-case.log")
    remote_matrix_path = str(output_path / "matrix-results.jsonl")
    for matrix_row in run_config.matrix:
        command = build_docker_run_command(
            image=run_config.config.docker_image,
            run_id=f"{run_config.run_id}-{matrix_row.key}",
            model_mount=remote_model_path,
            dataset_mount=remote_dataset_path,
            output_mount=output_path,
            proxy_url=proxy_url,
            command=_row_command(run_config, matrix_row.key),
        )
        commands.append(command)
        code, stdout, stderr = runner(spec, command, timeout)
        parsed = _parse_result(stdout)
        if code == 0 and parsed:
            row = VerlCaseResultRow.model_validate(
                {
                    "run_id": run_config.run_id,
                    "input_tokens": matrix_row.input_tokens,
                    "output_tokens": matrix_row.output_tokens,
                    "inference_mode": matrix_row.inference_mode,
                    "ignore_eos": matrix_row.ignore_eos,
                    **parsed,
                }
            )
        else:
            row = VerlCaseResultRow(
                run_id=run_config.run_id,
                input_tokens=matrix_row.input_tokens,
                output_tokens=matrix_row.output_tokens,
                inference_mode=matrix_row.inference_mode,
                ignore_eos=matrix_row.ignore_eos,
                status="failed",
                error=stderr or stdout or f"exit_code={code}",
                log_path=remote_log_path,
            )
        rows.append(row)

    ok = bool(rows) and all(row.status == "passed" for row in rows)
    return VerlCaseRunResult(
        ok=ok,
        run_id=run_config.run_id,
        rows=rows,
        commands=commands,
        remote_matrix_path=remote_matrix_path,
        remote_log_path=remote_log_path,
        error=None if ok else "one or more matrix rows failed",
    )


def _row_command(run_config: VerlCaseRunConfig, row_key: str) -> str:
    config_json = json.dumps(run_config.model_dump(mode="json"), ensure_ascii=False)
    script = (
        "python3 - <<'PY'\n"
        "import json\n"
        f"config = json.loads({config_json!r})\n"
        "assert config['config']['ignore_eos'] is False\n"
        f"print('VERL_CASE_ROW={row_key}')\n"
        "PY"
    )
    return "/bin/bash -lc " + shlex.quote(script)


def _parse_result(stdout: str) -> dict[str, object] | None:
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("VERL_CASE_RESULT="):
            return json.loads(line.split("=", 1)[1])
    return None
