"""Remote formal Verl case runner."""
from __future__ import annotations

import json
import shlex
import time
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field

from workspace_core.config import ServerSpec

from ..common.conda_utils import run_in_env, run_in_env_until_marker
from .case_config import (
    VerlCaseResultRow,
    VerlCaseRunConfig,
)
from .container_runtime import discover_reusable_container, reusable_exec_paths
from .docker import (
    build_docker_exec_command,
    build_docker_pull_command,
    build_docker_run_command,
)
from .source_sync import DependencySourceSyncError, filter_runtime_dependency_repo_paths, stage_dependency_sources
from .telemetry import DEFAULT_NPU_TELEMETRY_INTERVAL_SECONDS, build_npu_smi_watch_command


RemoteRunner = Callable[[ServerSpec, str, float], tuple[int, str, str]]
SourceSyncer = Callable[[ServerSpec, VerlCaseRunConfig], dict[str, str]]


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
    return run_in_env(spec, command, conda_env="", workdir=getattr(spec, "workdir", "") or "", timeout=timeout)


def _default_row_runner(spec: ServerSpec, command: str, timeout: float) -> tuple[int, str, str]:
    return run_in_env_until_marker(
        spec,
        command,
        marker="VERL_CASE_RESULT=",
        conda_env="",
        workdir=getattr(spec, "workdir", "") or "",
        timeout=timeout,
    )


def _default_source_syncer(spec: ServerSpec, run_config: VerlCaseRunConfig) -> dict[str, str]:
    return stage_dependency_sources(
        spec,
        run_id=run_config.run_id,
        remote_workdir=run_config.config.remote_workdir,
        dependency_repo_paths=filter_runtime_dependency_repo_paths(
            dependency_repo_paths=dict(run_config.config.dependency_repo_paths or {}),
            dependency_source_mounts=list(run_config.config.dependency_source_mounts or []),
            server=run_config.server,
            model_id=run_config.config.model_id,
            execution_profile=_execution_profile(run_config),
        ),
    )


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
    row_runner: RemoteRunner | None = None,
    source_syncer: SourceSyncer = _default_source_syncer,
) -> VerlCaseRunResult:
    """Run every strict matrix row on the remote host via Docker."""
    output_path = Path(remote_output_path or f"/home/t00906153/autoresearch/runs/{run_config.run_id}")
    commands: list[str] = []
    rows: list[VerlCaseResultRow] = []
    try:
        source_mounts = source_syncer(spec, run_config)
    except DependencySourceSyncError as exc:
        return VerlCaseRunResult(
            ok=False,
            run_id=run_config.run_id,
            commands=commands,
            rows=[],
            error=str(exc),
        )
    inspect = f"docker image inspect {shlex.quote(run_config.config.docker_image)} >/dev/null 2>&1"
    commands.append(inspect)
    inspect_code, _inspect_stdout, _inspect_stderr = runner(spec, inspect, min(timeout, 60.0))
    if inspect_code != 0:
        pull = build_docker_pull_command(
            run_config.config.docker_image,
            proxy_url=proxy_url,
        )
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

    reusable_container_name, _reusable_detail = discover_reusable_container(
        spec,
        image=run_config.config.docker_image,
        runner=runner,
        timeout=timeout,
    )
    execution_paths = _container_exec_paths(
        source_mounts=source_mounts,
        reusable_container_name=reusable_container_name,
        remote_model_path=remote_model_path,
        remote_dataset_path=remote_dataset_path,
        remote_output_path=output_path,
    )
    if bool(getattr(run_config.config, "cleanup_stale_verl_processes", True)):
        cleanup = _stale_verl_process_cleanup_command(output_path=output_path)
        commands.append(cleanup)
        cleanup_code, cleanup_stdout, cleanup_stderr = runner(spec, cleanup, min(timeout, 60.0))
        if cleanup_code != 0:
            return VerlCaseRunResult(
                ok=False,
                run_id=run_config.run_id,
                commands=commands,
                rows=[],
                error=cleanup_stderr or cleanup_stdout or "stale Verl process cleanup failed",
            )
    remote_log_path = str(output_path / "verl-case.log")
    remote_matrix_path = str(output_path / "matrix-results.jsonl")
    effective_row_runner = row_runner
    if effective_row_runner is None:
        effective_row_runner = _default_row_runner if runner is _default_runner else runner
    for matrix_row in run_config.matrix:
        row_command = _row_command(run_config, matrix_row.key, paths=execution_paths)
        row_device_count = int(getattr(matrix_row, "device_count", 0) or run_config.config.n_gpus_per_node)
        mount_device_count = max(row_device_count, int(run_config.config.n_gpus_per_node))
        if reusable_container_name:
            command = build_docker_exec_command(
                container_name=reusable_container_name,
                command=row_command,
            )
        else:
            command = build_docker_run_command(
                image=run_config.config.docker_image,
                run_id=f"{run_config.run_id}-{matrix_row.key}",
                model_mount=remote_model_path,
                dataset_mount=remote_dataset_path,
                output_mount=output_path,
                source_mounts=source_mounts,
                proxy_url=proxy_url,
                device_count=mount_device_count,
                command=row_command,
            )
        commands.append(command)
        try:
            if row_runner is None and runner is _default_runner:
                code, stdout, stderr = _run_row_with_result_polling(
                    spec,
                    command,
                    runner=runner,
                    output_path=output_path,
                    row_key=matrix_row.key,
                    timeout=timeout,
                )
            else:
                code, stdout, stderr = effective_row_runner(spec, command, timeout)
        except Exception as exc:  # pragma: no cover - exercised through integration SSH failures.
            code, stdout, stderr = 1, "", str(exc)
        parsed = _parse_result(stdout)
        if parsed is None:
            parsed = _read_remote_row_result(
                spec,
                runner,
                output_path=output_path,
                row_key=matrix_row.key,
                timeout=min(timeout, 60.0),
            )
        if parsed:
            row = VerlCaseResultRow.model_validate(
                {
                    "run_id": run_config.run_id,
                    "input_tokens": matrix_row.input_tokens,
                    "output_tokens": matrix_row.output_tokens,
                    "inference_mode": matrix_row.inference_mode,
                    "ignore_eos": matrix_row.ignore_eos,
                    **_matrix_row_result_metadata(matrix_row, run_config.config.training_steps),
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
                **_matrix_row_result_metadata(matrix_row, run_config.config.training_steps),
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


def _container_exec_paths(
    *,
    source_mounts: dict[str, str],
    reusable_container_name: str | None,
    remote_model_path: str | Path,
    remote_dataset_path: str | Path,
    remote_output_path: Path,
) -> dict[str, str]:
    if reusable_container_name:
        return reusable_exec_paths(
            source_mounts=source_mounts,
            remote_model_path=remote_model_path,
            remote_dataset_path=remote_dataset_path,
            remote_output_path=remote_output_path,
        )
    paths = {
        "verl_root": "/verl",
        "model_root": "/app/ckpt",
        "dataset_root": "/app/dataset",
        "output_root": "/app/output",
    }
    if "/veomni" in source_mounts:
        paths["veomni_root"] = "/veomni"
    return paths


def _row_command(
    run_config: VerlCaseRunConfig,
    row_key: str,
    *,
    paths: dict[str, str] | None = None,
) -> str:
    config_json = json.dumps(run_config.model_dump(mode="json"), ensure_ascii=False)
    script = _formal_row_script(
        config_json=config_json,
        row_key=row_key,
        execution_profile=_execution_profile(run_config),
        paths=paths or {},
        telemetry_command=build_npu_smi_watch_command(),
    )
    return "/bin/bash -lc " + shlex.quote(script)


def _matrix_row_result_metadata(matrix_row: object, target_training_steps: int) -> dict[str, object]:
    metadata: dict[str, object] = {
        "case_id": getattr(matrix_row, "key", None),
        "target_training_steps": target_training_steps,
    }
    for name in (
        "device_count",
        "visible_devices",
        "train_batch_size",
        "ppo_mini_batch_size",
        "ppo_micro_batch_size_per_gpu",
    ):
        value = getattr(matrix_row, name, None)
        if value is not None:
            metadata[name] = value
    return metadata


def _stale_verl_process_cleanup_command(*, output_path: str | Path = "/home/t00906153/autoresearch/runs") -> str:
    output_path = Path(output_path)
    run_root = output_path if output_path.name == "runs" else output_path.parent
    owned_markers = (f"{run_root.as_posix().rstrip('/')}/", "/tmp/ar-")
    script = (
        "import json\n"
        "import os\n"
        "import signal\n"
        "import subprocess\n"
        "import time\n"
        "\n"
        "self_pid = os.getpid()\n"
        "parent_pid = os.getppid()\n"
        "protected = {self_pid, parent_pid}\n"
        "result = subprocess.run(\n"
        "    ['ps', '-eo', 'pid=,ppid=,comm=,args='],\n"
        "    text=True,\n"
        "    stdout=subprocess.PIPE,\n"
        "    stderr=subprocess.DEVNULL,\n"
        "    check=False,\n"
        ")\n"
        "targets = []\n"
        f"owned_markers = {json.dumps(owned_markers)}\n"
        "target_names = {'VLLMWorker_TP', 'VLLM::Worker_TP', 'gqa_nonquant_pf', 'rayWorkerDict'}\n"
        "processes = {}\n"
        "children = {}\n"
        "for raw in result.stdout.splitlines():\n"
        "    parts = raw.strip().split(None, 3)\n"
        "    if len(parts) < 3:\n"
        "        continue\n"
        "    try:\n"
        "        pid = int(parts[0])\n"
        "        ppid = int(parts[1])\n"
        "    except ValueError:\n"
        "        continue\n"
        "    if pid in protected or ppid in protected:\n"
        "        continue\n"
        "    comm = parts[2]\n"
        "    args = parts[3] if len(parts) > 3 else ''\n"
        "    processes[pid] = (ppid, comm, args)\n"
        "    children.setdefault(ppid, []).append(pid)\n"
        "def _is_owned_pid(pid, seen=None):\n"
        "    seen = set() if seen is None else seen\n"
        "    if pid in seen or pid in protected:\n"
        "        return False\n"
        "    seen.add(pid)\n"
        "    item = processes.get(pid)\n"
        "    if item is None:\n"
        "        return False\n"
        "    ppid, _comm, args = item\n"
        "    if any(marker in args for marker in owned_markers):\n"
        "        return True\n"
        "    return _is_owned_pid(ppid, seen)\n"
        "for pid, (ppid, comm, args) in processes.items():\n"
        "    if pid in protected or ppid in protected:\n"
        "        continue\n"
        "    normalized_comm = comm.replace('::', '')\n"
        "    is_verl_target = (\n"
        "        comm.startswith('ray::')\n"
        "        or comm in target_names\n"
        "        or normalized_comm in target_names\n"
        "        or 'verl.trainer.main_ppo' in args\n"
        "    )\n"
        "    if is_verl_target and _is_owned_pid(pid):\n"
        "        targets.append(pid)\n"
        "smi = subprocess.run(\n"
        "    ['npu-smi', 'info'],\n"
        "    text=True,\n"
        "    stdout=subprocess.PIPE,\n"
        "    stderr=subprocess.DEVNULL,\n"
        "    check=False,\n"
        ")\n"
        "for raw in smi.stdout.splitlines():\n"
        "    if not any(name in raw for name in target_names):\n"
        "        continue\n"
        "    cells = [cell.strip() for cell in raw.split('|')]\n"
        "    for cell in cells:\n"
        "        if cell.isdigit():\n"
        "            pid = int(cell)\n"
        "            if pid not in protected and _is_owned_pid(pid):\n"
        "                targets.append(pid)\n"
        "            break\n"
        "targets = sorted(set(targets))\n"
        "for pid in targets:\n"
        "    try:\n"
        "        os.kill(pid, signal.SIGTERM)\n"
        "    except ProcessLookupError:\n"
        "        pass\n"
        "    except PermissionError:\n"
        "        pass\n"
        "time.sleep(3 if targets else 0)\n"
        "killed = []\n"
        "for pid in targets:\n"
        "    try:\n"
        "        os.kill(pid, 0)\n"
        "    except ProcessLookupError:\n"
        "        continue\n"
        "    except PermissionError:\n"
        "        continue\n"
        "    try:\n"
        "        os.kill(pid, signal.SIGKILL)\n"
        "        killed.append(pid)\n"
        "    except ProcessLookupError:\n"
        "        pass\n"
        "    except PermissionError:\n"
        "        pass\n"
        "print('AR_STALE_VERL_CLEANUP=' + json.dumps({'terminated': targets, 'sigkilled': killed}, sort_keys=True))\n"
    )
    return "python3 - <<'PY'\n" + script + "PY"


def _formal_row_script(
    *,
    config_json: str,
    row_key: str,
    execution_profile: str,
    paths: dict[str, str],
    telemetry_command: str,
) -> str:
    script = (
        "python3 - <<'PY'\n"
        "import datetime\n"
        "import glob\n"
        "import json\n"
        "import os\n"
        "import re\n"
        "import select\n"
        "import shlex\n"
        "import subprocess\n"
        "import sys\n"
        "import time\n"
        "import urllib.request\n"
        "from pathlib import Path\n"
        f"RUN_CONFIG = json.loads({config_json!r})\n"
        f"ROW_KEY = {row_key!r}\n"
        f"PROFILE = {execution_profile!r}\n"
        f"PATHS = json.loads({json.dumps(paths, ensure_ascii=False)!r})\n"
        f"TELEMETRY_COMMAND = {telemetry_command!r}\n"
        f"TELEMETRY_SAMPLE_INTERVAL_SECONDS = {DEFAULT_NPU_TELEMETRY_INTERVAL_SECONDS!r}\n"
        "PUSHGATEWAY_URL = str((RUN_CONFIG.get('extra') or {}).get('pushgateway_url') or '').strip()\n"
        "LAST_PUSHED_TELEMETRY_SAMPLE_INDEX = -1\n"
        "\n"
        "def _path(name, default):\n"
        "    value = PATHS.get(name)\n"
        "    return value if value else default\n"
        "\n"
        "def _case_bool(name):\n"
        "    value = case.get(name)\n"
        "    if value is None:\n"
        "        return None\n"
        "    if isinstance(value, bool):\n"
        "        return value\n"
        "    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}\n"
        "\n"
        "def _is_qwen35_model(case):\n"
        "    model_key = re.sub(r'[^a-z0-9.]+', '', str(case.get('model_id') or '').lower())\n"
        "    return 'qwen3.5' in model_key or 'qwen35' in model_key\n"
        "\n"
        "def _runtime_bool(name, default):\n"
        "    configured = _case_bool(name)\n"
        "    return default if configured is None else configured\n"
        "\n"
        "def _find_row():\n"
        "    for row in RUN_CONFIG['matrix']:\n"
        "        key = row.get('case_id') or f\"{row['inference_mode']}-{row['input_tokens']}-{row['output_tokens']}\"\n"
        "        if key == ROW_KEY:\n"
        "            return row\n"
        "    raise ValueError(f'unknown row key: {ROW_KEY}')\n"
        "\n"
        "def _token_slug(tokens):\n"
        "    tokens = int(tokens)\n"
        "    if tokens % 1024 == 0:\n"
        "        return f'{tokens // 1024}K'\n"
        "    return str(tokens)\n"
        "\n"
        "def _safe_slug(value):\n"
        "    value = re.sub(r'[^A-Za-z0-9._-]+', '-', value)\n"
        "    value = re.sub(r'-{2,}', '-', value)\n"
        "    return value.strip('-')\n"
        "\n"
        "def _model_slug(model_id):\n"
        "    name = str(model_id).rsplit('/', 1)[-1]\n"
        "    name = name.replace('Qwen3.5', 'Qwen35')\n"
        "    return _safe_slug(name) or 'model'\n"
        "\n"
        "def _timestamp_slug():\n"
        "    raw = str(RUN_CONFIG.get('created_at') or '')\n"
        "    match = re.match(r'^(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2})', raw)\n"
        "    if match:\n"
        "        year, month, day, hour, minute, second = match.groups()\n"
        "        return f'{year[-2:]}{month}{day}d-{hour}{minute}{second}s'\n"
        "    return 'unknown-time'\n"
        "\n"
        "def _wandb_run_name(case, row):\n"
        "    model = _model_slug(case.get('model_id', 'model'))\n"
        "    sequence = f\"{_token_slug(row['input_tokens'])}to{_token_slug(row['output_tokens'])}\"\n"
        "    val_mode = 'valonly' if bool(case.get('trainer_val_only', False)) else 'train'\n"
        "    eos = 'ignoreeos' if bool(row.get('ignore_eos', False)) else 'noignoreeos'\n"
        "    extras = []\n"
        "    if row.get('device_count'):\n"
        "        extras.append(f\"{int(row['device_count'])}npu\")\n"
        "    if row.get('train_batch_size'):\n"
        "        extras.append(f\"bs{int(row['train_batch_size'])}\")\n"
        "    if row.get('ppo_mini_batch_size'):\n"
        "        extras.append(f\"mini{int(row['ppo_mini_batch_size'])}\")\n"
        "    if row.get('ppo_micro_batch_size_per_gpu'):\n"
        "        extras.append(f\"micro{int(row['ppo_micro_batch_size_per_gpu'])}\")\n"
        "    suffix = '-' + '-'.join(extras) if extras else ''\n"
        "    return _safe_slug(f\"{model}-GRPO-{sequence}-{_timestamp_slug()}-{val_mode}-{row['inference_mode']}-{eos}{suffix}\")\n"
        "\n"
        "def _run(command, *, cwd=None, env=None, log_path=None, timeout_seconds=None, telemetry_context=None):\n"
        "    if cwd is None:\n"
        "        cwd = _path('verl_root', '/verl')\n"
        "    shell = 'source /usr/local/Ascend/ascend-toolkit/set_env.sh >/dev/null 2>&1 || true; '\n"
        "    shell += 'source /usr/local/Ascend/nnal/atb/set_env.sh >/dev/null 2>&1 || true; '\n"
        "    shell += command\n"
        "    output = []\n"
        "    log_handle = None\n"
        "    if log_path:\n"
        "        Path(log_path).parent.mkdir(parents=True, exist_ok=True)\n"
        "        log_handle = open(log_path, 'a', encoding='utf-8')\n"
        "        log_handle.write('\\n__AR_COMMAND__=' + command + '\\n')\n"
        "        log_handle.flush()\n"
        "    def _emit(text):\n"
        "        output.append(text)\n"
        "        if log_handle:\n"
        "            log_handle.write(text)\n"
        "            log_handle.flush()\n"
        "    started_at = time.monotonic()\n"
        "    try:\n"
        "        proc = subprocess.Popen(\n"
        "            ['bash', '-lc', shell], cwd=cwd, env=env, text=True, bufsize=1,\n"
        "            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\n"
        "        )\n"
        "        last_telemetry_push = 0.0\n"
        "        while True:\n"
        "            if proc.stdout is not None:\n"
        "                ready, _, _ = select.select([proc.stdout], [], [], min(1.0, TELEMETRY_SAMPLE_INTERVAL_SECONDS))\n"
        "                if ready:\n"
        "                    line = proc.stdout.readline()\n"
        "                    if line:\n"
        "                        _emit(line)\n"
        "            if telemetry_context is not None and time.monotonic() - last_telemetry_push >= TELEMETRY_SAMPLE_INTERVAL_SECONDS:\n"
        "                _push_live_telemetry(**telemetry_context)\n"
        "                last_telemetry_push = time.monotonic()\n"
        "            returncode = proc.poll()\n"
        "            if returncode is not None:\n"
        "                if proc.stdout is not None:\n"
        "                    rest = proc.stdout.read()\n"
        "                    if rest:\n"
        "                        _emit(rest)\n"
        "                return subprocess.CompletedProcess(['bash', '-lc', shell], returncode, stdout=''.join(output))\n"
        "            if timeout_seconds and time.monotonic() - started_at > timeout_seconds:\n"
        "                _emit(f'\\n__AR_TIMEOUT__={int(timeout_seconds)}s\\n')\n"
        "                proc.terminate()\n"
        "                try:\n"
        "                    proc.wait(timeout=10)\n"
        "                except subprocess.TimeoutExpired:\n"
        "                    proc.kill()\n"
        "                    proc.wait(timeout=10)\n"
        "                if proc.stdout is not None:\n"
        "                    rest = proc.stdout.read()\n"
        "                    if rest:\n"
        "                        _emit(rest)\n"
        "                return subprocess.CompletedProcess(['bash', '-lc', shell], 124, stdout=''.join(output))\n"
        "    finally:\n"
        "        if log_handle:\n"
        "            log_handle.close()\n"
        "\n"
        "def _latest_jsonl(path):\n"
        "    files = sorted(glob.glob(str(Path(path) / '*.jsonl')))\n"
        "    return Path(files[-1]) if files else None\n"
        "\n"
        "def _load_generations(path):\n"
        "    if not path or not path.exists():\n"
        "        return []\n"
        "    rows = []\n"
        "    for line in path.read_text(encoding='utf-8').splitlines():\n"
        "        if line.strip():\n"
        "            rows.append(json.loads(line))\n"
        "    return rows\n"
        "\n"
        "def _mean_score(rows):\n"
        "    scores = []\n"
        "    for row in rows:\n"
        "        value = row.get('acc', row.get('score'))\n"
        "        if isinstance(value, (int, float)):\n"
        "            scores.append(float(value))\n"
        "    return sum(scores) / len(scores) if scores else None\n"
        "\n"
        "def _metric_from_log(text):\n"
        "    patterns = [\n"
        "        r\"val-core/[^']*/acc/[^']*': ([0-9.]+)\",\n"
        "        r'val-core/[^\\\"]*/acc/[^\\\"]*\\\": ([0-9.]+)',\n"
        "        r\"val-core/[^=]*/acc/[^=]*=([0-9.]+)\",\n"
        "    ]\n"
        "    for pattern in patterns:\n"
        "        matches = re.findall(pattern, text)\n"
        "        if matches:\n"
        "            return float(matches[-1])\n"
        "    return None\n"
        "\n"
        "def _completed_training_steps_from_log(text):\n"
        "    numbers = []\n"
        "    patterns = [\n"
        "        r'(?<![\\w/-])global[_ -]?step\\s*(?:[:=]|\\s)\\s*(\\d+)\\b',\n"
        "        r'(?<![\\w/-])training[_ -]?step\\s*[:=]?\\s*(\\d+)(?:\\s*/\\s*\\d+)?\\b',\n"
        "        r'(?<![\\w/-])step\\s*[:=]\\s*(\\d+)\\b',\n"
        "        r'(?<![\\w/-])step\\s+(\\d+)\\s*/\\s*\\d+\\b',\n"
        "        r'training progress:.*?(\\d+)\\s*/\\s*(\\d+)',\n"
        "    ]\n"
        "    for line in text.splitlines():\n"
        "        lowered_line = line.lower()\n"
        "        if '__ar_command__=' in lowered_line or 'total_training_steps' in lowered_line or 'total training steps' in lowered_line:\n"
        "            continue\n"
        "        for pattern in patterns:\n"
        "            for match in re.findall(pattern, line, flags=re.IGNORECASE):\n"
        "                try:\n"
        "                    if isinstance(match, tuple):\n"
        "                        numbers.append(int(match[0]))\n"
        "                        continue\n"
        "                    numbers.append(int(match))\n"
        "                except (TypeError, ValueError):\n"
        "                    pass\n"
        "    return max(numbers) if numbers else 0\n"
        "\n"
        "def _metric_value_from_line(line, key):\n"
        "    pattern = re.compile(r'(?<![A-Za-z0-9_./-])' + re.escape(key) + r'\\s*[:=]\\s*([-+]?[0-9]+(?:\\.[0-9]+)?)', flags=re.IGNORECASE)\n"
        "    match = pattern.search(line)\n"
        "    if not match:\n"
        "        return None\n"
        "    try:\n"
        "        return float(match.group(1))\n"
        "    except ValueError:\n"
        "        return None\n"
        "\n"
        "def _step_from_line(line):\n"
        "    for pattern in (\n"
        "        r'global[_ -]?step[^0-9]{0,20}(\\d+)',\n"
        "        r'training[_ -]?step[^0-9]{0,20}(\\d+)',\n"
        "        r'\\bstep\\s*[:=]\\s*(\\d+)\\b',\n"
        "        r'\\bstep\\s+(\\d+)\\s*/\\s*\\d+\\b',\n"
        "    ):\n"
        "        match = re.search(pattern, line, flags=re.IGNORECASE)\n"
        "        if match:\n"
        "            try:\n"
        "                return int(match.group(1))\n"
        "            except (TypeError, ValueError):\n"
        "                return None\n"
        "    return None\n"
        "\n"
        "def _step_time_key_priority(key):\n"
        "    normalized = str(key).lower().replace('-', '_')\n"
        "    order = ('perf/time_per_step', 'timing_s/step', 'timing/step', 'time_per_step', 'step_time')\n"
        "    for index, item in enumerate(order):\n"
        "        if normalized == item:\n"
        "            return index\n"
        "    return len(order)\n"
        "\n"
        "def _step_seconds_from_line(line):\n"
        "    candidates = []\n"
        "    for key in ('perf/time_per_step', 'perf/time-per-step', 'timing_s/step', 'timing/step', 'time_per_step', 'step_time'):\n"
        "        value = _metric_value_from_line(line, key)\n"
        "        if value is None:\n"
        "            continue\n"
        "        seconds = value / 1000.0 if key.endswith('_ms') or key.endswith('-ms') else value\n"
        "        candidates.append((_step_time_key_priority(key), seconds, key))\n"
        "    if not candidates:\n"
        "        return None, ''\n"
        "    _priority, seconds, key = min(candidates, key=lambda item: item[0])\n"
        "    return seconds, key\n"
        "\n"
        "def _steady_state_throughput(text, *, train_batch_size, output_tokens, device_count, step_start=3, step_end=5):\n"
        "    selected = {}\n"
        "    for line in text.splitlines():\n"
        "        step = _step_from_line(line)\n"
        "        if step is None or step < step_start or step > step_end:\n"
        "            continue\n"
        "        seconds, time_key = _step_seconds_from_line(line)\n"
        "        if seconds is None or seconds <= 0:\n"
        "            continue\n"
        "        seq_mean = _metric_value_from_line(line, 'global_seqlen/mean')\n"
        "        if seq_mean is not None and seq_mean > 0:\n"
        "            tokens = seq_mean * max(1, int(train_batch_size))\n"
        "            token_source = 'global_seqlen_mean'\n"
        "        else:\n"
        "            tokens = max(1, int(output_tokens)) * max(1, int(train_batch_size))\n"
        "            token_source = 'output_tokens_fallback'\n"
        "        current = selected.get(step)\n"
        "        priority = _step_time_key_priority(time_key)\n"
        "        if current is None or priority < int(current['priority']):\n"
        "            selected[step] = {'seconds': seconds, 'tokens': tokens, 'token_source': token_source, 'time_key': time_key, 'priority': priority}\n"
        "    if not selected:\n"
        "        return None\n"
        "    total_seconds = sum(float(item['seconds']) for item in selected.values())\n"
        "    if total_seconds <= 0:\n"
        "        return None\n"
        "    total_tokens = sum(float(item['tokens']) for item in selected.values())\n"
        "    npu_count = max(1, int(device_count))\n"
        "    tps = total_tokens / total_seconds\n"
        "    token_sources = {str(item['token_source']) for item in selected.values()}\n"
        "    return {\n"
        "        'step_start': step_start, 'step_end': step_end, 'step_count': len(selected),\n"
        "        'total_tokens': total_tokens, 'total_seconds': total_seconds,\n"
        "        'tokens_per_second': tps, 'tokens_per_second_per_npu': tps / npu_count,\n"
        "        'token_source': 'mixed' if len(token_sources) > 1 else next(iter(token_sources)),\n"
        "        'time_keys': sorted({str(item['time_key']) for item in selected.values()}),\n"
        "    }\n"
        "\n"
        "def _failure_class(returncode, sample_count, completed_steps, target_steps, trainer_val_only, log_text):\n"
        "    lower_log = log_text.lower()\n"
        "    if 'resource_busy' in lower_log or 'resources are busy' in lower_log or '507899' in lower_log:\n"
        "        return 'resource_busy'\n"
        "    if 'no available memory for the cache blocks' in lower_log or ('to serve at least one request' in lower_log and 'kv cache' in lower_log):\n"
        "        return 'vllm_kv_cache_memory'\n"
        "    if 'af_unix path length cannot exceed' in lower_log or 'validate_socket_filename failed' in lower_log:\n"
        "        return 'ray_socket_path_length'\n"
        "    if 'not enough disk space' in lower_log or 'available space: 0 gb' in lower_log:\n"
        "        return 'disk_space'\n"
        "    if 'mamba cache align mode' in lower_log and 'max_num_batched_tokens' in lower_log:\n"
        "        return 'vllm_mamba_block_size'\n"
        "    if 'enginedeaderror' in lower_log and ('aicpu exception' in lower_log or '507018' in lower_log):\n"
        "        if 'hccl watchdog' in lower_log:\n"
        "            return 'vllm_engine_dead_aicpu_hccl'\n"
        "        return 'vllm_engine_dead_aicpu'\n"
        "    if (\n"
        "        ('start (0) + length (1024) exceeds dimension size (512)' in lower_log or 'start out of range' in lower_log)\n"
        "        and ('update_weights' in lower_log or 'load_weights' in lower_log or 'bucketed_weight_transfer' in lower_log)\n"
        "    ):\n"
        "        return 'vllm_update_weights_shape_mismatch'\n"
        "    if 'aclrtmallocphysical failed' in lower_log and 'camem_allocator.cpp' in lower_log:\n"
        "        if 'update_weights' in lower_log or 'rollout.resume' in lower_log or 'wake_up' in lower_log:\n"
        "            return 'vllm_camem_update_weights_oom'\n"
        "        return 'vllm_camem_allocator_oom'\n"
        "    if 'out of memory' in lower_log or 'oom' in lower_log or 'aclrtmalloc' in lower_log:\n"
        "        return 'oom'\n"
        "    if returncode == 124:\n"
        "        return 'timeout'\n"
        "    if returncode != 0:\n"
        "        return 'verl_exit'\n"
        "    if trainer_val_only and sample_count <= 0:\n"
        "        return 'no_validation_samples'\n"
        "    if not trainer_val_only and completed_steps < target_steps:\n"
        "        return 'incomplete_training_steps'\n"
        "    return None\n"
        "\n"
        "def _consistency(rows, baseline_path):\n"
        "    baseline = _load_generations(Path(baseline_path))\n"
        "    if not rows or not baseline:\n"
        "        return None\n"
        "    total = min(len(rows), len(baseline))\n"
        "    if total <= 0:\n"
        "        return None\n"
        "    same = 0\n"
        "    for left, right in zip(rows[:total], baseline[:total]):\n"
        "        if str(left.get('output', '')).strip() == str(right.get('output', '')).strip():\n"
        "            same += 1\n"
        "    return same / total\n"
        "\n"
        "def _start_telemetry_sampler(raw_path, env):\n"
        "    Path(raw_path).parent.mkdir(parents=True, exist_ok=True)\n"
        "    handle = open(raw_path, 'w', encoding='utf-8')\n"
        "    shell = 'source /usr/local/Ascend/ascend-toolkit/set_env.sh >/dev/null 2>&1 || true; '\n"
        "    shell += TELEMETRY_COMMAND\n"
        "    try:\n"
        "        proc = subprocess.Popen(\n"
        "            ['bash', '-lc', shell], cwd=_path('verl_root', '/verl'), env=env, text=True,\n"
        "            stdout=handle, stderr=subprocess.STDOUT,\n"
        "        )\n"
        "        return proc, handle\n"
        "    except Exception as exc:\n"
        "        handle.write(f'__AR_TELEMETRY_START_FAILED__={exc}\\n')\n"
        "        handle.close()\n"
        "        return None, None\n"
        "\n"
        "def _stop_telemetry_sampler(proc, handle):\n"
        "    if proc is not None and proc.poll() is None:\n"
        "        proc.terminate()\n"
        "        try:\n"
        "            proc.wait(timeout=5)\n"
        "        except subprocess.TimeoutExpired:\n"
        "            proc.kill()\n"
        "            proc.wait(timeout=5)\n"
        "    if handle is not None:\n"
        "        handle.close()\n"
        "\n"
        "def _telemetry_cells(line):\n"
        "    if '|' not in line:\n"
        "        return []\n"
        "    cells = [cell.strip() for cell in line.strip().strip('|').split('|')]\n"
        "    if not cells or all(cell and set(cell) <= {'-', '+', ' '} for cell in cells):\n"
        "        return []\n"
        "    return cells\n"
        "\n"
        "def _telemetry_key(value):\n"
        "    return re.sub(r'[^a-z0-9]+', '', value.lower())\n"
        "\n"
        "def _telemetry_column(value):\n"
        "    key = _telemetry_key(value)\n"
        "    if key in {'npuid', 'deviceid', 'id'} or key == 'npu':\n"
        "        return 'device_id'\n"
        "    if key in {'chip', 'chipid', 'chipphyid', 'phyid'}:\n"
        "        return 'chip_id'\n"
        "    if 'aicore' in key:\n"
        "        return 'ai_core_utilization_percent'\n"
        "    if 'npu' in key and ('util' in key or 'usage' in key):\n"
        "        return 'npu_utilization_percent'\n"
        "    if 'hbm' in key or 'memory' in key:\n"
        "        if 'used' in key:\n"
        "            return 'hbm_used_mib'\n"
        "        if 'total' in key or 'capacity' in key:\n"
        "            return 'hbm_total_mib'\n"
        "        return 'memory'\n"
        "    return None\n"
        "\n"
        "def _telemetry_columns(cells):\n"
        "    columns = {}\n"
        "    for index, cell in enumerate(cells):\n"
        "        column = _telemetry_column(cell)\n"
        "        if column:\n"
        "            columns[column] = index\n"
        "    return columns if 'device_id' in columns else {}\n"
        "\n"
        "def _telemetry_number(value):\n"
        "    match = re.search(r'-?\\d+(?:\\.\\d+)?', value or '')\n"
        "    return float(match.group(0)) if match else None\n"
        "\n"
        "def _telemetry_number_at(cells, index):\n"
        "    if index is None or index >= len(cells):\n"
        "        return None\n"
        "    return _telemetry_number(cells[index])\n"
        "\n"
        "def _telemetry_memory(cells, columns):\n"
        "    used = _telemetry_number_at(cells, columns.get('hbm_used_mib'))\n"
        "    total = _telemetry_number_at(cells, columns.get('hbm_total_mib'))\n"
        "    memory_index = columns.get('memory')\n"
        "    if memory_index is not None and memory_index < len(cells):\n"
        "        parts = re.split(r'\\s*/\\s*', cells[memory_index])\n"
        "        if len(parts) == 2:\n"
        "            used = used if used is not None else _telemetry_number(parts[0])\n"
        "            total = total if total is not None else _telemetry_number(parts[1])\n"
        "    return used, total\n"
        "\n"
        "def _telemetry_info_device_id(cells):\n"
        "    if len(cells) < 3 or not re.fullmatch(r'\\d+\\s+\\S+', cells[0]):\n"
        "        return None\n"
        "    if not re.search(r'\\bOK\\b|FAIL|WARN', cells[1], flags=re.IGNORECASE):\n"
        "        return None\n"
        "    match = re.match(r'(\\d+)', cells[0])\n"
        "    return int(match.group(1)) if match else None\n"
        "\n"
        "def _telemetry_info_sample(cells, device_id, raw_line):\n"
        "    if len(cells) < 3:\n"
        "        return None\n"
        "    identity = [int(item) for item in re.findall(r'\\d+', cells[0])]\n"
        "    if not identity:\n"
        "        return None\n"
        "    chip_id = identity[1] if len(identity) > 1 else identity[0]\n"
        "    values = [float(item) for item in re.findall(r'\\d+(?:\\.\\d+)?', cells[2])]\n"
        "    if len(values) < 5:\n"
        "        return None\n"
        "    return {\n"
        "        'run_id': RUN_CONFIG['run_id'], 'case_id': ROW_KEY, 'server': RUN_CONFIG.get('server'),\n"
        "        'device_id': int(device_id), 'sample_index': 0, 'source': 'npu-smi-watch',\n"
        "        'chip_id': chip_id,\n"
        "        'hbm_used_mib': values[-2], 'hbm_total_mib': values[-1],\n"
        "        'ai_core_utilization_percent': values[0], 'npu_utilization_percent': None,\n"
        "        'raw_line': raw_line.strip(),\n"
        "    }\n"
        "\n"
        "def _write_telemetry_jsonl(raw_path, jsonl_path):\n"
        "    columns = {}\n"
        "    pending_info_device_id = None\n"
        "    rows = []\n"
        "    if not Path(raw_path).exists():\n"
        "        return {'sample_count': 0, 'device_count': 0, 'sample_interval_seconds': TELEMETRY_SAMPLE_INTERVAL_SECONDS, 'source': 'npu-smi-watch'}\n"
        "    for line in Path(raw_path).read_text(encoding='utf-8', errors='replace').splitlines():\n"
        "        cells = _telemetry_cells(line)\n"
        "        if not cells:\n"
        "            continue\n"
        "        info_device_id = _telemetry_info_device_id(cells)\n"
        "        if info_device_id is not None:\n"
        "            pending_info_device_id = info_device_id\n"
        "            continue\n"
        "        if pending_info_device_id is not None:\n"
        "            info_sample = _telemetry_info_sample(cells, pending_info_device_id, line)\n"
        "            pending_info_device_id = None\n"
        "            if info_sample is not None:\n"
        "                info_sample['sample_index'] = len(rows)\n"
        "                rows.append(info_sample)\n"
        "                continue\n"
        "        maybe_columns = _telemetry_columns(cells)\n"
        "        if maybe_columns:\n"
        "            columns = maybe_columns\n"
        "            continue\n"
        "        device_id = _telemetry_number_at(cells, columns.get('device_id')) if columns else None\n"
        "        if device_id is None:\n"
        "            continue\n"
        "        chip_id = _telemetry_number_at(cells, columns.get('chip_id')) if columns else None\n"
        "        hbm_used, hbm_total = _telemetry_memory(cells, columns)\n"
        "        rows.append({\n"
        "            'run_id': RUN_CONFIG['run_id'], 'case_id': ROW_KEY, 'server': RUN_CONFIG.get('server'),\n"
        "            'device_id': int(device_id), 'sample_index': len(rows), 'source': 'npu-smi-watch',\n"
        "            'chip_id': int(chip_id) if chip_id is not None else None,\n"
        "            'hbm_used_mib': hbm_used, 'hbm_total_mib': hbm_total,\n"
        "            'ai_core_utilization_percent': _telemetry_number_at(cells, columns.get('ai_core_utilization_percent')),\n"
        "            'npu_utilization_percent': _telemetry_number_at(cells, columns.get('npu_utilization_percent')),\n"
        "            'raw_line': line.strip(),\n"
        "        })\n"
        "    Path(jsonl_path).write_text(''.join(json.dumps(row, ensure_ascii=False) + '\\n' for row in rows), encoding='utf-8')\n"
        "    def _max_value(key):\n"
        "        values = [row.get(key) for row in rows if row.get(key) is not None]\n"
        "        return max(values) if values else None\n"
        "    return {\n"
        "        'sample_count': len(rows), 'device_count': len({(row['device_id'], row.get('chip_id', 0) or 0) for row in rows}),\n"
        "        'sample_interval_seconds': TELEMETRY_SAMPLE_INTERVAL_SECONDS, 'source': 'npu-smi-watch',\n"
        "        'max_hbm_used_mib': _max_value('hbm_used_mib'),\n"
        "        'hbm_total_mib': _max_value('hbm_total_mib'),\n"
        "        'max_ai_core_utilization_percent': _max_value('ai_core_utilization_percent'),\n"
        "        'max_npu_utilization_percent': _max_value('npu_utilization_percent'),\n"
        "    }\n"
        "\n"
        "def _telemetry_rows_from_raw(raw_path):\n"
        "    columns = {}\n"
        "    pending_info_device_id = None\n"
        "    rows = []\n"
        "    if not Path(raw_path).exists():\n"
        "        return rows\n"
        "    for line in Path(raw_path).read_text(encoding='utf-8', errors='replace').splitlines():\n"
        "        cells = _telemetry_cells(line)\n"
        "        if not cells:\n"
        "            continue\n"
        "        info_device_id = _telemetry_info_device_id(cells)\n"
        "        if info_device_id is not None:\n"
        "            pending_info_device_id = info_device_id\n"
        "            continue\n"
        "        if pending_info_device_id is not None:\n"
        "            info_sample = _telemetry_info_sample(cells, pending_info_device_id, line)\n"
        "            pending_info_device_id = None\n"
        "            if info_sample is not None:\n"
        "                info_sample['sample_index'] = len(rows)\n"
        "                rows.append(info_sample)\n"
        "                continue\n"
        "        maybe_columns = _telemetry_columns(cells)\n"
        "        if maybe_columns:\n"
        "            columns = maybe_columns\n"
        "            continue\n"
        "        device_id = _telemetry_number_at(cells, columns.get('device_id')) if columns else None\n"
        "        if device_id is None:\n"
        "            continue\n"
        "        chip_id = _telemetry_number_at(cells, columns.get('chip_id')) if columns else None\n"
        "        hbm_used, hbm_total = _telemetry_memory(cells, columns)\n"
        "        rows.append({\n"
        "            'run_id': RUN_CONFIG['run_id'], 'case_id': ROW_KEY, 'server': RUN_CONFIG.get('server'),\n"
        "            'device_id': int(device_id), 'sample_index': len(rows), 'source': 'npu-smi-watch',\n"
        "            'chip_id': int(chip_id) if chip_id is not None else None,\n"
        "            'hbm_used_mib': hbm_used, 'hbm_total_mib': hbm_total,\n"
        "            'ai_core_utilization_percent': _telemetry_number_at(cells, columns.get('ai_core_utilization_percent')),\n"
        "            'npu_utilization_percent': _telemetry_number_at(cells, columns.get('npu_utilization_percent')),\n"
        "            'raw_line': line.strip(),\n"
        "        })\n"
        "    return rows\n"
        "\n"
        "def _prom_escape(value):\n"
        "    return str(value).replace('\\\\', '\\\\\\\\').replace('\"', '\\\\\"').replace('\\n', '\\\\n')\n"
        "\n"
        "def _prom_labels(items):\n"
        "    return ','.join(f'{key}=\"{_prom_escape(value)}\"' for key, value in items.items() if value is not None)\n"
        "\n"
        "def _prom_job_suffix(value):\n"
        "    value = re.sub(r'[^A-Za-z0-9_.-]+', '_', str(value)).strip('_')\n"
        "    return value or 'unknown'\n"
        "\n"
        "def _latest_by_device(rows):\n"
        "    latest = {}\n"
        "    for item in rows:\n"
        "        key = (item.get('server'), item.get('device_id'), item.get('chip_id', 0) or 0, item.get('source'))\n"
        "        latest[key] = item\n"
        "    return list(latest.values())\n"
        "\n"
        "def _telemetry_metric_lines(rows, wandb_run_name):\n"
        "    experiment_lines = [\n"
        "        '# TYPE autoresearch_npu_hbm_used_mib gauge',\n"
        "        '# TYPE autoresearch_npu_hbm_total_mib gauge',\n"
        "        '# TYPE autoresearch_npu_aicore_utilization_percent gauge',\n"
        "        '# TYPE autoresearch_npu_utilization_percent gauge',\n"
        "        '# TYPE autoresearch_experiment_case_info gauge',\n"
        "        '# TYPE autoresearch_experiment_case_latest_sample_index gauge',\n"
        "    ]\n"
        "    machine_lines = [\n"
        "        '# TYPE autoresearch_machine_npu_hbm_used_mib gauge',\n"
        "        '# TYPE autoresearch_machine_npu_hbm_total_mib gauge',\n"
        "        '# TYPE autoresearch_machine_npu_aicore_utilization_percent gauge',\n"
        "        '# TYPE autoresearch_machine_npu_utilization_percent gauge',\n"
        "    ]\n"
        "    latest = _latest_by_device(rows)\n"
        "    latest_sample_index = max((int(item.get('sample_index') or 0) for item in rows), default=0)\n"
        "    case_labels = _prom_labels({\n"
        "        'run_id': RUN_CONFIG['run_id'], 'case_id': ROW_KEY, 'server': RUN_CONFIG.get('server'),\n"
        "        'wandb_project': wandb_project, 'wandb_run_name': wandb_run_name,\n"
        "    })\n"
        "    experiment_lines.append(f'autoresearch_experiment_case_info{{{case_labels}}} 1')\n"
        "    experiment_lines.append(f'autoresearch_experiment_case_latest_sample_index{{{case_labels}}} {latest_sample_index:g}')\n"
        "    for item in latest:\n"
        "        exp_labels = _prom_labels({\n"
        "            'run_id': item.get('run_id'), 'case_id': item.get('case_id'), 'server': item.get('server'),\n"
        "            'device_id': item.get('device_id'), 'chip_id': item.get('chip_id'), 'source': item.get('source'),\n"
        "        })\n"
        "        machine_labels = _prom_labels({\n"
        "            'server': item.get('server'), 'device_id': item.get('device_id'), 'chip_id': item.get('chip_id', 0), 'source': item.get('source'),\n"
        "        })\n"
        "        pairs = [\n"
        "            ('hbm_used_mib', 'autoresearch_npu_hbm_used_mib', 'autoresearch_machine_npu_hbm_used_mib'),\n"
        "            ('hbm_total_mib', 'autoresearch_npu_hbm_total_mib', 'autoresearch_machine_npu_hbm_total_mib'),\n"
        "            ('ai_core_utilization_percent', 'autoresearch_npu_aicore_utilization_percent', 'autoresearch_machine_npu_aicore_utilization_percent'),\n"
        "            ('npu_utilization_percent', 'autoresearch_npu_utilization_percent', 'autoresearch_machine_npu_utilization_percent'),\n"
        "        ]\n"
        "        for key, exp_name, machine_name in pairs:\n"
        "            value = item.get(key)\n"
        "            if value is None:\n"
        "                continue\n"
        "            experiment_lines.append(f'{exp_name}{{{exp_labels}}} {float(value):g}')\n"
        "            machine_lines.append(f'{machine_name}{{{machine_labels}}} {float(value):g}')\n"
        "    return '\\n'.join(experiment_lines + ['']), '\\n'.join(machine_lines + [''])\n"
        "\n"
        "def _push_prometheus_text(endpoint, body, method='POST'):\n"
        "    if not endpoint or not body.strip():\n"
        "        return False\n"
        "    try:\n"
        "        req = urllib.request.Request(endpoint, data=body.encode('utf-8'), method=method)\n"
        "        with urllib.request.urlopen(req, timeout=2.0) as resp:\n"
        "            return 200 <= resp.status < 300\n"
        "    except Exception:\n"
        "        return False\n"
        "\n"
        "def _push_live_telemetry(raw_path, wandb_run_name, force=False):\n"
        "    global LAST_PUSHED_TELEMETRY_SAMPLE_INDEX\n"
        "    if not PUSHGATEWAY_URL:\n"
        "        return False\n"
        "    rows = _telemetry_rows_from_raw(raw_path)\n"
        "    if not rows:\n"
        "        return False\n"
        "    latest_sample_index = max(int(item.get('sample_index') or 0) for item in rows)\n"
        "    if not force and latest_sample_index <= LAST_PUSHED_TELEMETRY_SAMPLE_INDEX:\n"
        "        return False\n"
        "    experiment_body, machine_body = _telemetry_metric_lines(rows, wandb_run_name)\n"
        "    run_endpoint = PUSHGATEWAY_URL.rstrip('/') + '/metrics/job/ar_' + _prom_job_suffix(RUN_CONFIG['run_id'])\n"
        "    machine_endpoint = PUSHGATEWAY_URL.rstrip('/') + '/metrics/job/autoresearch_machine/server/' + _prom_job_suffix(RUN_CONFIG.get('server'))\n"
        "    ok = _push_prometheus_text(run_endpoint, experiment_body, method='POST')\n"
        "    ok = _push_prometheus_text(machine_endpoint, machine_body, method='PUT') or ok\n"
        "    if ok:\n"
        "        LAST_PUSHED_TELEMETRY_SAMPLE_INDEX = latest_sample_index\n"
        "    return ok\n"
        "\n"
        "row = _find_row()\n"
        "case = RUN_CONFIG['config']\n"
        "assert case['ignore_eos'] is False\n"
        "wandb_project = str(case.get('wandb_project') or 'verl')\n"
        "wandb_run_name = _wandb_run_name(case, row)\n"
        "output_root = Path(_path('output_root', '/app/output'))\n"
        "row_dir = output_root / 'rows' / ROW_KEY\n"
        "log_path = row_dir / f\"{RUN_CONFIG['run_id']}-{ROW_KEY}.log\"\n"
        "telemetry_raw_path = row_dir / 'npu-smi-watch.raw.log'\n"
        "telemetry_jsonl_path = row_dir / 'npu-telemetry.jsonl'\n"
        "validation_dir = row_dir / 'validation'\n"
        "data_dir = output_root / 'data' / 'geo3k'\n"
        "ray_run_id = ''.join(ch for ch in RUN_CONFIG['run_id'] if ch.isalnum())[-12:] or 'run'\n"
        "ray_row_id = ''.join(ch for ch in ROW_KEY if ch.isalnum())[-12:] or 'row'\n"
        "ray_tmp_target = output_root / 'ray_tmp' / f'ar-{ray_run_id}-{ray_row_id}'\n"
        "ray_tmp_root = Path('/tmp') / f'ar-{ray_run_id[-6:]}-{ray_row_id[-6:]}'\n"
        "for item in (row_dir, validation_dir, data_dir, ray_tmp_target):\n"
        "    item.mkdir(parents=True, exist_ok=True)\n"
        "try:\n"
        "    if ray_tmp_root.is_symlink() or ray_tmp_root.exists():\n"
        "        if ray_tmp_root.is_symlink() or ray_tmp_root.is_file():\n"
        "            ray_tmp_root.unlink()\n"
        "        elif ray_tmp_root.resolve() != ray_tmp_target.resolve():\n"
        "            raise RuntimeError(f'RAY_TMPDIR path exists and is not ours: {ray_tmp_root}')\n"
        "    if not ray_tmp_root.exists():\n"
        "        ray_tmp_root.symlink_to(ray_tmp_target, target_is_directory=True)\n"
        "except OSError:\n"
        "    ray_tmp_root = ray_tmp_target\n"
        "env = os.environ.copy()\n"
        "env.update({\n"
        "    'HF_HOME': str(output_root / 'hf_cache'),\n"
        "    'TRANSFORMERS_CACHE': str(output_root / 'hf_cache' / 'transformers'),\n"
        "    'HF_DATASETS_CACHE': str(output_root / 'hf_cache' / 'datasets'),\n"
        "    'PYTHONUNBUFFERED': '1',\n"
        "    'HCCL_CONNECT_TIMEOUT': '1500',\n"
        "    'HCCL_HOST_SOCKET_PORT_RANGE': '60000-60050',\n"
        "    'HCCL_NPU_SOCKET_PORT_RANGE': '61000-61050',\n"
        "    'RAY_TMPDIR': str(ray_tmp_root),\n"
        "    'RAY_EXPERIMENTAL_NOSET_ASCEND_RT_VISIBLE_DEVICES': '1',\n"
        "    'WANDB_DIR': str(output_root / 'wandb'),\n"
        "    'WANDB_MODE': 'offline',\n"
        "    'VLLM_USE_V1': '1',\n"
        "    'VLLM_VERSION': '0.9.1',\n"
        "    'TASK_QUEUE_ENABLE': '2',\n"
        "    'CPU_AFFINITY_CONF': '1',\n"
        "})\n"
        "if PROFILE == 'veomni':\n"
        "    env.update({\n"
        "        'TASK_QUEUE_ENABLE': '1',\n"
        "        'HCCL_OP_EXPANSION_MODE': 'AIV',\n"
        "    })\n"
        "    veomni_root = PATHS.get('veomni_root', '/veomni')\n"
        "    if veomni_root and Path(veomni_root).exists():\n"
        "        extra_pythonpath = veomni_root\n"
        "        current_pythonpath = env.get('PYTHONPATH')\n"
        "        env['PYTHONPATH'] = extra_pythonpath if not current_pythonpath else extra_pythonpath + os.pathsep + current_pythonpath\n"
        "model_root = Path(_path('model_root', '/app/ckpt'))\n"
        "dataset_root = Path(_path('dataset_root', '/app/dataset'))\n"
        "model_path = str(model_root) if (model_root / 'config.json').exists() else case['model_id']\n"
        "mounted_train = dataset_root / 'geo3k' / 'train.parquet'\n"
        "mounted_test = dataset_root / 'geo3k' / 'test.parquet'\n"
        "if mounted_train.exists() and mounted_test.exists():\n"
        "    train_file, test_file = mounted_train, mounted_test\n"
        "elif (dataset_root / 'train.parquet').exists() and (dataset_root / 'test.parquet').exists():\n"
        "    train_file, test_file = dataset_root / 'train.parquet', dataset_root / 'test.parquet'\n"
        "else:\n"
        "    train_file, test_file = data_dir / 'train.parquet', data_dir / 'test.parquet'\n"
        "    if not train_file.exists() or not test_file.exists():\n"
        "        prep_cmd = 'python3 examples/data_preprocess/geo3k.py --local_save_dir ' + shlex.quote(str(data_dir))\n"
        "        prep = _run(prep_cmd, env=env, log_path=log_path)\n"
        "        if prep.returncode != 0:\n"
        "            raise RuntimeError('geo3k preprocess failed')\n"
        "configured_n_gpus = int(case.get('n_gpus_per_node', 8))\n"
        "visible_devices = row.get('visible_devices') or list(range(int(row.get('device_count') or configured_n_gpus)))\n"
        "visible_devices = [int(device) for device in visible_devices]\n"
        "n_gpus = max(1, len(visible_devices))\n"
        "ascend_visible_devices = ','.join(str(index) for index in visible_devices)\n"
        "if row.get('train_batch_size') is not None:\n"
        "    train_batch_size = int(row['train_batch_size'])\n"
        "else:\n"
        "    train_batch_size = max(int(case.get('train_batch_size', 8)), n_gpus)\n"
        "train_max_samples = max(int(case.get('train_max_samples', train_batch_size)), train_batch_size)\n"
        "ppo_mini_batch_size = int(row.get('ppo_mini_batch_size') or 1)\n"
        "ppo_micro_batch_size_per_gpu = int(row.get('ppo_micro_batch_size_per_gpu') or 1)\n"
        "rollout_n = int(row.get('rollout_n') or case.get('rollout_n', 1))\n"
        "configured_agent_workers = int(row.get('agent_num_workers') or case.get('agent_num_workers', 8))\n"
        "agent_num_workers = max(1, min(configured_agent_workers, train_batch_size))\n"
        "while train_batch_size % agent_num_workers != 0 and agent_num_workers > 1:\n"
        "    agent_num_workers -= 1\n"
        "trainer_val_only = bool(case.get('trainer_val_only', False))\n"
        "target_training_steps = 0 if trainer_val_only else int(case.get('training_steps', 3))\n"
        "effective_training_steps = max(1, target_training_steps)\n"
        "val_batch_size = int(case.get('val_batch_size', 1))\n"
        "configured_rollout_max_num_seqs = case.get('rollout_max_num_seqs')\n"
        "rollout_max_num_seqs = int(configured_rollout_max_num_seqs) if configured_rollout_max_num_seqs is not None else max(1, val_batch_size, train_batch_size)\n"
        "rollout_max_num_seqs = max(1, rollout_max_num_seqs)\n"
        "row_timeout_seconds = int(case.get('row_timeout_seconds', 1800))\n"
        "is_async = row['inference_mode'] == 'async'\n"
        "max_tokens = int(row['input_tokens']) + int(row['output_tokens']) + 1\n"
        "rollout_max_model_len_floor = int(case.get('rollout_max_model_len_floor', 24576))\n"
        "ppo_max_token_len_per_gpu_floor = int(case.get('ppo_max_token_len_per_gpu_floor', 24576))\n"
        "ppo_max_token_len_per_gpu = max(max_tokens, ppo_max_token_len_per_gpu_floor)\n"
        "rollout_max_model_len = max(max_tokens, rollout_max_model_len_floor)\n"
        "rollout_max_num_batched_tokens = rollout_max_model_len\n"
        "rollout_gpu_memory_utilization = float(case.get('rollout_gpu_memory_utilization', 0.5))\n"
        "rollout_update_weights_bucket_megabytes = int(case.get('rollout_update_weights_bucket_megabytes', 2048))\n"
        "tensor_parallel_size = min(max(1, int(case.get('tensor_model_parallel_size', 2))), n_gpus)\n"
        "rollout_data_parallel_size = max(1, n_gpus // tensor_parallel_size)\n"
        "qwen35_compat = PROFILE == 'fsdp' and _is_qwen35_model(case)\n"
        "use_remove_padding = _runtime_bool('use_remove_padding', PROFILE != 'veomni' and not qwen35_compat)\n"
        "use_dynamic_bsz = _runtime_bool('use_dynamic_bsz', PROFILE != 'veomni' and not qwen35_compat)\n"
        "fsdp2_offload_policy = _runtime_bool('fsdp2_offload_policy', False)\n"
        "rollout_free_cache_engine = _runtime_bool('rollout_free_cache_engine', True)\n"
        "env['ASCEND_RT_VISIBLE_DEVICES'] = ascend_visible_devices\n"
        "args = [\n"
        "    'python3', '-m', 'verl.trainer.main_ppo',\n"
        "    '--config-path=config', '--config-name=ppo_trainer.yaml',\n"
        "    'algorithm.adv_estimator=grpo',\n"
        "    'algorithm.use_kl_in_reward=False',\n"
        "    f'data.train_files={str(train_file)}',\n"
        "    f'data.val_files={str(test_file)}',\n"
        "    f'data.train_batch_size={train_batch_size}',\n"
        "    f'data.train_max_samples={train_max_samples}',\n"
        "    f'data.val_max_samples={int(case.get(\"val_max_samples\", 2))}',\n"
        "    f'data.max_prompt_length={int(row[\"input_tokens\"])}',\n"
        "    f'data.max_response_length={int(row[\"output_tokens\"])}',\n"
        "    'data.filter_overlong_prompts=True', 'data.truncation=error',\n"
        "    'data.image_key=images', 'data.shuffle=False', 'data.validation_shuffle=False',\n"
        "    'data.return_raw_chat=True',\n"
        "    'data.dataloader_num_workers=1',\n"
        "    f'actor_rollout_ref.model.path={model_path}',\n"
        "    f'actor_rollout_ref.model.use_remove_padding={str(use_remove_padding)}',\n"
        "    'actor_rollout_ref.model.use_fused_kernels=False',\n"
        "    'actor_rollout_ref.model.enable_gradient_checkpointing=True',\n"
        "    'actor_rollout_ref.actor.optim.lr=1e-6',\n"
        "    f'actor_rollout_ref.actor.ppo_mini_batch_size={ppo_mini_batch_size}',\n"
        "    f'actor_rollout_ref.actor.ppo_max_token_len_per_gpu={ppo_max_token_len_per_gpu}',\n"
        "    f'actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu={ppo_micro_batch_size_per_gpu}',\n"
        "    f'actor_rollout_ref.actor.use_dynamic_bsz={str(use_dynamic_bsz)}',\n"
        "    'actor_rollout_ref.actor.use_kl_loss=True',\n"
        "    'actor_rollout_ref.actor.kl_loss_coef=0.01',\n"
        "    'actor_rollout_ref.actor.kl_loss_type=low_var_kl',\n"
        "    'actor_rollout_ref.actor.entropy_coeff=0',\n"
        "    'actor_rollout_ref.actor.use_torch_compile=False',\n"
        "    'actor_rollout_ref.rollout.name=vllm',\n"
        "    'actor_rollout_ref.rollout.ignore_eos=False',\n"
        "    f'actor_rollout_ref.rollout.max_model_len={rollout_max_model_len}',\n"
        "    f'actor_rollout_ref.rollout.max_num_batched_tokens={rollout_max_num_batched_tokens}',\n"
        "    f'actor_rollout_ref.rollout.max_num_seqs={rollout_max_num_seqs}',\n"
        "    f'actor_rollout_ref.rollout.log_prob_use_dynamic_bsz={str(use_dynamic_bsz)}',\n"
        "    f'actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu={ppo_max_token_len_per_gpu}',\n"
        "    'actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=1',\n"
        "    f'actor_rollout_ref.rollout.tensor_model_parallel_size={tensor_parallel_size}',\n"
        "    f'actor_rollout_ref.rollout.gpu_memory_utilization={rollout_gpu_memory_utilization}',\n"
        "    f'actor_rollout_ref.rollout.checkpoint_engine.update_weights_bucket_megabytes={rollout_update_weights_bucket_megabytes}',\n"
        "    'actor_rollout_ref.rollout.enable_chunked_prefill=False',\n"
        "    'actor_rollout_ref.rollout.enforce_eager=True',\n"
        "    f'actor_rollout_ref.rollout.free_cache_engine={str(rollout_free_cache_engine)}',\n"
        "    f'actor_rollout_ref.rollout.n={rollout_n}',\n"
        "    f'actor_rollout_ref.rollout.agent.num_workers={agent_num_workers}',\n"
        "    f'actor_rollout_ref.rollout.val_kwargs.n={rollout_n}',\n"
        "    'actor_rollout_ref.rollout.val_kwargs.do_sample=False',\n"
        "    f'actor_rollout_ref.ref.log_prob_use_dynamic_bsz={str(use_dynamic_bsz)}',\n"
        "    f'actor_rollout_ref.ref.log_prob_max_token_len_per_gpu={ppo_max_token_len_per_gpu}',\n"
        "    'actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=1',\n"
        "    'trainer.critic_warmup=0',\n"
        "    'trainer.balance_batch=True',\n"
        "    'trainer.device=npu',\n"
        "    'trainer.logger=[console,wandb]',\n"
        "    f'trainer.project_name={wandb_project}',\n"
        "    f'trainer.experiment_name={wandb_run_name}',\n"
        "    f'trainer.n_gpus_per_node={n_gpus}',\n"
        "    'trainer.nnodes=1', 'trainer.save_freq=-1', 'trainer.test_freq=-1',\n"
        "    'trainer.total_epochs=1', f'trainer.total_training_steps={effective_training_steps}',\n"
        "    f'trainer.val_only={str(trainer_val_only)}',\n"
        "    f'trainer.val_before_train={str(trainer_val_only)}', 'trainer.resume_mode=disable',\n"
        "    f'trainer.validation_data_dir={str(validation_dir)}',\n"
        "    f'trainer.default_local_dir={str(row_dir / \"ckpt\")}',\n"
        "]\n"
        "if PROFILE == 'veomni':\n"
        "    veomni_init_device = 'meta' if n_gpus > 1 else 'npu'\n"
        "    args.extend([\n"
        "        'model_engine=veomni',\n"
        "        '+trainer.use_legacy_worker_impl=disable',\n"
        "        'actor_rollout_ref.actor.veomni.param_offload=True',\n"
        "        'actor_rollout_ref.actor.veomni.optimizer_offload=True',\n"
        "        f'actor_rollout_ref.actor.veomni.fsdp_size={n_gpus}',\n"
        "        f'actor_rollout_ref.actor.veomni.init_device={veomni_init_device}',\n"
        "        'actor_rollout_ref.actor.veomni.ulysses_parallel_size=1',\n"
        "        'actor_rollout_ref.actor.veomni.expert_parallel_size=1',\n"
        "        'actor_rollout_ref.actor.veomni.attn_implementation=flash_attention_2',\n"
        "        'actor_rollout_ref.actor.veomni.cross_entropy_loss_implementation=npu',\n"
        "        'actor_rollout_ref.actor.veomni.rms_norm_implementation=npu',\n"
        "        'actor_rollout_ref.actor.veomni.rotary_pos_emb_implementation=npu',\n"
        "        'actor_rollout_ref.actor.veomni.swiglu_mlp_implementation=eager',\n"
        "        'actor_rollout_ref.actor.veomni.load_balancing_loss_implementation=eager',\n"
        "        'actor_rollout_ref.actor.veomni.rms_norm_gated_implementation=eager',\n"
        "        'actor_rollout_ref.actor.veomni.causal_conv1d_implementation=eager',\n"
        "        'actor_rollout_ref.actor.veomni.chunk_gated_delta_rule_implementation=eager',\n"
        "        'actor_rollout_ref.ref.veomni.param_offload=True',\n"
        "        'actor_rollout_ref.ref.veomni.optimizer_offload=True',\n"
        "        f'actor_rollout_ref.ref.veomni.init_device={veomni_init_device}',\n"
        "        'actor_rollout_ref.ref.use_torch_compile=False',\n"
        "        f'actor_rollout_ref.rollout.data_parallel_size={rollout_data_parallel_size}',\n"
        "        'actor_rollout_ref.rollout.expert_parallel_size=1',\n"
        "    ])\n"
        "else:\n"
        "    fsdp_strategy = 'fsdp2' if PROFILE == 'fsdp2' else 'fsdp'\n"
        "    args.extend([\n"
        "        f'actor_rollout_ref.actor.strategy={fsdp_strategy}',\n"
        "        'actor_rollout_ref.actor.fsdp_config.param_offload=True',\n"
        "        'actor_rollout_ref.actor.fsdp_config.optimizer_offload=True',\n"
        "        'actor_rollout_ref.ref.fsdp_config.param_offload=True',\n"
        "    ])\n"
        "    if PROFILE == 'fsdp2' and fsdp2_offload_policy:\n"
        "        args.append('actor_rollout_ref.actor.fsdp_config.offload_policy=True')\n"
        "if is_async:\n"
        "    args.append('actor_rollout_ref.rollout.mode=async')\n"
        "cmd = ' '.join(shlex.quote(str(item)) for item in args)\n"
        "started_wall = datetime.datetime.now(datetime.timezone.utc)\n"
        "started = time.monotonic()\n"
        "telemetry_proc, telemetry_handle = _start_telemetry_sampler(telemetry_raw_path, env)\n"
        "telemetry_context = {'raw_path': telemetry_raw_path, 'wandb_run_name': wandb_run_name}\n"
        "try:\n"
        "    proc = _run(cmd, env=env, log_path=log_path, timeout_seconds=row_timeout_seconds, telemetry_context=telemetry_context)\n"
        "finally:\n"
        "    _stop_telemetry_sampler(telemetry_proc, telemetry_handle)\n"
        "    _push_live_telemetry(force=True, **telemetry_context)\n"
        "finished_wall = datetime.datetime.now(datetime.timezone.utc)\n"
        "elapsed = time.monotonic() - started\n"
        "telemetry_summary = _write_telemetry_jsonl(telemetry_raw_path, telemetry_jsonl_path)\n"
        "log_text = Path(log_path).read_text(encoding='utf-8', errors='replace') if Path(log_path).exists() else ''\n"
        "generation_path = _latest_jsonl(validation_dir)\n"
        "generations = _load_generations(generation_path)\n"
        "sample_count = len(generations)\n"
        "accuracy = _metric_from_log(log_text)\n"
        "if accuracy is None:\n"
        "    accuracy = _mean_score(generations)\n"
        "consistency = 1.0 if row['inference_mode'] == 'sync' else _consistency(\n"
        "    generations, output_root / 'rows' / f\"sync-{row['input_tokens']}-{row['output_tokens']}\" / 'validation' / '0.jsonl'\n"
        ")\n"
        "completed_training_steps = 0 if trainer_val_only else _completed_training_steps_from_log(log_text)\n"
        "steady = _steady_state_throughput(\n"
        "    log_text,\n"
        "    train_batch_size=train_batch_size,\n"
        "    output_tokens=int(row['output_tokens']),\n"
        "    device_count=n_gpus,\n"
        "    step_start=3,\n"
        "    step_end=5,\n"
        ")\n"
        "failure_class = _failure_class(proc.returncode, sample_count, completed_training_steps, target_training_steps, trainer_val_only, log_text)\n"
        "status = 'passed' if failure_class is None else 'failed'\n"
        "if status == 'passed':\n"
        "    error = None\n"
        "elif proc.returncode == 124:\n"
        "    error = f'verl timeout after {row_timeout_seconds}s; samples={sample_count}; steps={completed_training_steps}/{target_training_steps}'\n"
        "elif failure_class == 'incomplete_training_steps':\n"
        "    error = f'verl incomplete training steps={completed_training_steps}/{target_training_steps}'\n"
        "else:\n"
        "    error = f'verl exit={proc.returncode}; samples={sample_count}; steps={completed_training_steps}/{target_training_steps}'\n"
        "result = {\n"
        "    'status': status,\n"
        "    'started_at': started_wall.isoformat().replace('+00:00', 'Z'),\n"
        "    'finished_at': finished_wall.isoformat().replace('+00:00', 'Z'),\n"
        "    'started_at_unix': started_wall.timestamp(),\n"
        "    'finished_at_unix': finished_wall.timestamp(),\n"
        "    'elapsed_seconds': elapsed,\n"
        "    'tokens_per_second': (sample_count * int(row['output_tokens']) / elapsed) if elapsed > 0 and sample_count else None,\n"
        "    'latency_ms': (elapsed * 1000 / sample_count) if sample_count else None,\n"
        "    'sample_count': sample_count,\n"
        "    'completed_training_steps': completed_training_steps,\n"
        "    'target_training_steps': target_training_steps,\n"
        "    'steady_state_step_start': steady.get('step_start') if steady else 3,\n"
        "    'steady_state_step_end': steady.get('step_end') if steady else 5,\n"
        "    'steady_state_step_count': steady.get('step_count') if steady else 0,\n"
        "    'steady_state_total_tokens': steady.get('total_tokens') if steady else None,\n"
        "    'steady_state_total_seconds': steady.get('total_seconds') if steady else None,\n"
        "    'steady_state_tokens_per_second': steady.get('tokens_per_second') if steady else None,\n"
        "    'steady_state_tokens_per_second_per_npu': steady.get('tokens_per_second_per_npu') if steady else None,\n"
        "    'steady_state_token_source': steady.get('token_source') if steady else None,\n"
        "    'steady_state_time_keys': steady.get('time_keys') if steady else [],\n"
        "    'device_count': n_gpus,\n"
        "    'visible_devices': visible_devices,\n"
        "    'train_batch_size': train_batch_size,\n"
        "    'ppo_mini_batch_size': ppo_mini_batch_size,\n"
        "    'ppo_micro_batch_size_per_gpu': ppo_micro_batch_size_per_gpu,\n"
        "    'agent_num_workers': agent_num_workers,\n"
        "    'failure_class': failure_class,\n"
        "    'accuracy': accuracy,\n"
        "    'consistency': consistency,\n"
        "    'log_path': str(log_path),\n"
        "    'telemetry_raw_path': str(telemetry_raw_path),\n"
        "    'telemetry_jsonl_path': str(telemetry_jsonl_path),\n"
        "    'telemetry_summary': telemetry_summary,\n"
        "    'error': error,\n"
        "}\n"
        "result_path = row_dir / 'result.json'\n"
        "result_path.write_text(json.dumps(result, ensure_ascii=False) + '\\n', encoding='utf-8')\n"
        "print('VERL_CASE_RESULT=' + json.dumps(result, ensure_ascii=False))\n"
        "PY"
    )
    return script


def _read_remote_row_result(
    spec: ServerSpec,
    runner: RemoteRunner,
    *,
    output_path: Path,
    row_key: str,
    timeout: float,
) -> dict[str, object] | None:
    result_path = output_path / "rows" / row_key / "result.json"
    quoted = shlex.quote(str(result_path))
    code, stdout, _stderr = runner(spec, f"test -f {quoted} && cat {quoted}", timeout)
    if code != 0:
        return None
    text = stdout.strip()
    if not text:
        return None
    try:
        return json.loads(text.splitlines()[-1])
    except json.JSONDecodeError:
        return None


def _run_row_with_result_polling(
    spec: ServerSpec,
    command: str,
    *,
    runner: RemoteRunner,
    output_path: Path,
    row_key: str,
    timeout: float,
    poll_interval: float = 10.0,
) -> tuple[int, str, str]:
    row_dir = output_path / "rows" / row_key
    result_path = row_dir / "result.json"
    exit_path = row_dir / "launcher.exit"
    pid_path = row_dir / "launcher.pid"
    stdout_path = row_dir / "launcher.stdout"
    stderr_path = row_dir / "launcher.stderr"
    host_telemetry_raw_path = row_dir / "host-npu-smi-watch.raw.log"
    host_telemetry_pid_path = row_dir / "host-npu-smi-watch.pid"
    quoted = {
        path: shlex.quote(str(path))
        for path in (
            row_dir,
            result_path,
            exit_path,
            pid_path,
            stdout_path,
            stderr_path,
            host_telemetry_raw_path,
            host_telemetry_pid_path,
        )
    }
    prepare = (
        f"mkdir -p {quoted[row_dir]} && "
        f"rm -f {quoted[result_path]} {quoted[exit_path]} {quoted[pid_path]} "
        f"{quoted[stdout_path]} {quoted[stderr_path]} "
        f"{quoted[host_telemetry_raw_path]} {quoted[host_telemetry_pid_path]}"
    )
    prepare_code, prepare_stdout, prepare_stderr = runner(spec, prepare, min(timeout, 60.0))
    if prepare_code != 0:
        return prepare_code, prepare_stdout, prepare_stderr

    host_telemetry_command = build_npu_smi_watch_command(include_host_metrics=True)
    start_host_telemetry = (
        f"setsid nohup /bin/bash -lc {shlex.quote(host_telemetry_command)} "
        f"> {quoted[host_telemetry_raw_path]} 2>&1 < /dev/null & "
        f"pid=$!; echo $pid > {quoted[host_telemetry_pid_path]}; "
        "echo AR_HOST_TELEMETRY_PID=$pid"
    )
    _telemetry_code, telemetry_stdout, telemetry_stderr = runner(
        spec,
        start_host_telemetry,
        min(timeout, 30.0),
    )
    last_stdout = telemetry_stdout
    last_stderr = telemetry_stderr

    launcher_shell = f"{command}; ec=$?; echo $ec > {quoted[exit_path]}; exit $ec"
    launch = (
        f"setsid nohup /bin/bash -lc {shlex.quote(launcher_shell)} "
        f"> {quoted[stdout_path]} 2> {quoted[stderr_path]} < /dev/null & "
        f"pid=$!; echo $pid > {quoted[pid_path]}; echo AR_ROW_PID=$pid"
    )
    try:
        launch_code, launch_stdout, launch_stderr = runner(spec, launch, min(timeout, 60.0))
        if launch_code != 0:
            return launch_code, launch_stdout, launch_stderr

        deadline = time.monotonic() + timeout
        last_stdout = launch_stdout or last_stdout
        last_stderr = launch_stderr or last_stderr
        while time.monotonic() < deadline:
            code, stdout, stderr = runner(
                spec,
                f"test -f {quoted[result_path]} && cat {quoted[result_path]}",
                min(timeout, 30.0),
            )
            if code == 0 and stdout.strip():
                return 0, "VERL_CASE_RESULT=" + stdout.strip().splitlines()[-1], stderr
            last_stdout, last_stderr = stdout or last_stdout, stderr or last_stderr

            exit_code, exit_stdout, exit_stderr = runner(
                spec,
                f"test -f {quoted[exit_path]} && cat {quoted[exit_path]}",
                min(timeout, 30.0),
            )
            if exit_code == 0 and exit_stdout.strip():
                tail_cmd = (
                    f"tail -80 {quoted[stderr_path]} 2>/dev/null; "
                    f"tail -80 {quoted[stdout_path]} 2>/dev/null"
                )
                _tail_code, tail_stdout, tail_stderr = runner(spec, tail_cmd, min(timeout, 30.0))
                detail = tail_stderr or tail_stdout or exit_stderr or exit_stdout
                return int(exit_stdout.strip().splitlines()[-1] or "1"), "", detail

            time.sleep(min(poll_interval, max(0.1, deadline - time.monotonic())))

        return 124, last_stdout, last_stderr or f"row polling timeout after {timeout}s"
    finally:
        _stop_host_telemetry_sampler(
            spec,
            runner,
            pid_path=host_telemetry_pid_path,
            timeout=min(timeout, 30.0),
        )


def _stop_host_telemetry_sampler(
    spec: ServerSpec,
    runner: RemoteRunner,
    *,
    pid_path: Path,
    timeout: float,
) -> None:
    quoted_pid_path = shlex.quote(str(pid_path))
    command = (
        f"if test -f {quoted_pid_path}; then "
        f"pid=$(cat {quoted_pid_path} 2>/dev/null | tail -1); "
        "if test -n \"$pid\"; then "
        "children=$(pgrep -P \"$pid\" 2>/dev/null || true); "
        "for child in $children; do kill \"$child\" 2>/dev/null || true; done; "
        "kill \"$pid\" 2>/dev/null || true; "
        "sleep 1; "
        "for child in $children; do kill -9 \"$child\" 2>/dev/null || true; done; "
        "kill -9 \"$pid\" 2>/dev/null || true; "
        "fi; "
        f"rm -f {quoted_pid_path}; "
        "fi"
    )
    try:
        runner(spec, command, timeout)
    except Exception:
        return


def _parse_result(stdout: str) -> dict[str, object] | None:
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("VERL_CASE_RESULT="):
            return json.loads(line.split("=", 1)[1])
    return None


def _execution_profile(run_config: VerlCaseRunConfig) -> str:
    profile = str(
        (run_config.extra or {}).get("execution_profile")
        or getattr(run_config.config, "execution_profile", "fsdp")
        or "fsdp"
    ).strip().lower()
    if profile and profile != "auto":
        return profile
    return "fsdp"
