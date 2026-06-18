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
from .container_runtime import discover_reusable_container, reusable_exec_paths
from .docker import (
    build_docker_exec_command,
    build_docker_pull_command,
    build_docker_run_command,
)
from .source_sync import DependencySourceSyncError, filter_dependency_repo_paths, stage_dependency_sources


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
    return run_in_env(spec, command, conda_env=getattr(spec, "conda_env", "") or "", workdir=getattr(spec, "workdir", "") or "", timeout=timeout)


def _default_source_syncer(spec: ServerSpec, run_config: VerlCaseRunConfig) -> dict[str, str]:
    return stage_dependency_sources(
        spec,
        run_id=run_config.run_id,
        remote_workdir=run_config.config.remote_workdir,
        dependency_repo_paths=filter_dependency_repo_paths(
            dependency_repo_paths=dict(run_config.config.dependency_repo_paths or {}),
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
    remote_log_path = str(output_path / "verl-case.log")
    remote_matrix_path = str(output_path / "matrix-results.jsonl")
    for matrix_row in run_config.matrix:
        row_command = _row_command(run_config, matrix_row.key, paths=execution_paths)
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
                command=row_command,
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
    )
    return "/bin/bash -lc " + shlex.quote(script)


def _formal_row_script(
    *,
    config_json: str,
    row_key: str,
    execution_profile: str,
    paths: dict[str, str],
) -> str:
    script = (
        "python3 - <<'PY'\n"
        "import glob\n"
        "import json\n"
        "import os\n"
        "import re\n"
        "import select\n"
        "import shlex\n"
        "import subprocess\n"
        "import sys\n"
        "import time\n"
        "from pathlib import Path\n"
        f"RUN_CONFIG = json.loads({config_json!r})\n"
        f"ROW_KEY = {row_key!r}\n"
        f"PROFILE = {execution_profile!r}\n"
        f"PATHS = json.loads({json.dumps(json.dumps(paths), ensure_ascii=False)!r})\n"
        "\n"
        "def _path(name, default):\n"
        "    value = PATHS.get(name)\n"
        "    return value if value else default\n"
        "\n"
        "def _find_row():\n"
        "    for row in RUN_CONFIG['matrix']:\n"
        "        key = f\"{row['inference_mode']}-{row['input_tokens']}-{row['output_tokens']}\"\n"
        "        if key == ROW_KEY:\n"
        "            return row\n"
        "    raise ValueError(f'unknown row key: {ROW_KEY}')\n"
        "\n"
        "def _run(command, *, cwd=None, env=None, log_path=None, timeout_seconds=None):\n"
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
        "        while True:\n"
        "            if proc.stdout is not None:\n"
        "                ready, _, _ = select.select([proc.stdout], [], [], 1.0)\n"
        "                if ready:\n"
        "                    line = proc.stdout.readline()\n"
        "                    if line:\n"
        "                        _emit(line)\n"
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
        "row = _find_row()\n"
        "case = RUN_CONFIG['config']\n"
        "assert case['ignore_eos'] is False\n"
        "output_root = Path(_path('output_root', '/app/output'))\n"
        "row_dir = output_root / 'rows' / ROW_KEY\n"
        "log_path = row_dir / 'verl.log'\n"
        "validation_dir = row_dir / 'validation'\n"
        "data_dir = output_root / 'data' / 'geo3k'\n"
        "for item in (row_dir, validation_dir, data_dir):\n"
        "    item.mkdir(parents=True, exist_ok=True)\n"
        "env = os.environ.copy()\n"
        "env.update({\n"
        "    'HF_HOME': str(output_root / 'hf_cache'),\n"
        "    'TRANSFORMERS_CACHE': str(output_root / 'hf_cache' / 'transformers'),\n"
        "    'HF_DATASETS_CACHE': str(output_root / 'hf_cache' / 'datasets'),\n"
        "    'PYTHONUNBUFFERED': '1',\n"
        "    'HCCL_CONNECT_TIMEOUT': '1500',\n"
        "    'HCCL_HOST_SOCKET_PORT_RANGE': '60000-60050',\n"
        "    'HCCL_NPU_SOCKET_PORT_RANGE': '61000-61050',\n"
        "    'RAY_TMPDIR': str(output_root / 'ray_tmp'),\n"
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
        "n_gpus = int(case.get('n_gpus_per_node', 8))\n"
        "ascend_visible_devices = ','.join(str(index) for index in range(n_gpus))\n"
        "train_batch_size = max(int(case.get('train_batch_size', 8)), n_gpus)\n"
        "train_max_samples = max(int(case.get('train_max_samples', 8)), train_batch_size)\n"
        "val_batch_size = int(case.get('val_batch_size', 1))\n"
        "row_timeout_seconds = int(case.get('row_timeout_seconds', 1800))\n"
        "max_tokens = int(row['input_tokens']) + int(row['output_tokens']) + 1\n"
        "ppo_max_token_len_per_gpu = max(max_tokens, 24576)\n"
        "rollout_max_model_len = max(max_tokens, 24576)\n"
        "tensor_parallel_size = max(1, int(case.get('tensor_model_parallel_size', 2)))\n"
        "rollout_data_parallel_size = max(1, n_gpus // tensor_parallel_size)\n"
        "use_remove_padding = PROFILE != 'veomni'\n"
        "use_dynamic_bsz = PROFILE != 'veomni'\n"
        "env['ASCEND_RT_VISIBLE_DEVICES'] = ascend_visible_devices\n"
        "is_async = row['inference_mode'] == 'async'\n"
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
        "    'actor_rollout_ref.actor.ppo_mini_batch_size=1',\n"
        "    f'actor_rollout_ref.actor.ppo_max_token_len_per_gpu={ppo_max_token_len_per_gpu}',\n"
        "    'actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=1',\n"
        "    f'actor_rollout_ref.actor.use_dynamic_bsz={str(use_dynamic_bsz)}',\n"
        "    'actor_rollout_ref.actor.use_kl_loss=True',\n"
        "    'actor_rollout_ref.actor.kl_loss_coef=0.01',\n"
        "    'actor_rollout_ref.actor.kl_loss_type=low_var_kl',\n"
        "    'actor_rollout_ref.actor.entropy_coeff=0',\n"
        "    'actor_rollout_ref.actor.use_torch_compile=False',\n"
        "    'actor_rollout_ref.rollout.name=vllm',\n"
        "    'actor_rollout_ref.rollout.ignore_eos=False',\n"
        "    f'actor_rollout_ref.rollout.max_model_len={rollout_max_model_len}',\n"
        "    f'actor_rollout_ref.rollout.max_num_batched_tokens={rollout_max_model_len}',\n"
        "    f'actor_rollout_ref.rollout.max_num_seqs={max(1, val_batch_size)}',\n"
        "    f'actor_rollout_ref.rollout.log_prob_use_dynamic_bsz={str(use_dynamic_bsz)}',\n"
        "    f'actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu={ppo_max_token_len_per_gpu}',\n"
        "    'actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=1',\n"
        "    f'actor_rollout_ref.rollout.tensor_model_parallel_size={tensor_parallel_size}',\n"
        "    'actor_rollout_ref.rollout.gpu_memory_utilization=0.5',\n"
        "    'actor_rollout_ref.rollout.enable_chunked_prefill=False',\n"
        "    'actor_rollout_ref.rollout.enforce_eager=True',\n"
        "    'actor_rollout_ref.rollout.free_cache_engine=True',\n"
        "    f'actor_rollout_ref.rollout.n={int(case.get(\"rollout_n\", 1))}',\n"
        "    f'actor_rollout_ref.rollout.val_kwargs.n={int(case.get(\"rollout_n\", 1))}',\n"
        "    'actor_rollout_ref.rollout.val_kwargs.do_sample=False',\n"
        "    f'actor_rollout_ref.ref.log_prob_use_dynamic_bsz={str(use_dynamic_bsz)}',\n"
        "    f'actor_rollout_ref.ref.log_prob_max_token_len_per_gpu={ppo_max_token_len_per_gpu}',\n"
        "    'actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=1',\n"
        "    'trainer.critic_warmup=0',\n"
        "    'trainer.balance_batch=True',\n"
        "    'trainer.device=npu',\n"
        "    'trainer.logger=[console,wandb]',\n"
        "    f'trainer.project_name=autoresearch_verl_case',\n"
        "    f'trainer.experiment_name={RUN_CONFIG[\"run_id\"]}_{ROW_KEY}',\n"
        "    f'trainer.n_gpus_per_node={n_gpus}',\n"
        "    'trainer.nnodes=1', 'trainer.save_freq=-1', 'trainer.test_freq=-1',\n"
        "    'trainer.total_epochs=1', 'trainer.total_training_steps=1',\n"
        "    f'trainer.val_only={str(bool(case.get(\"trainer_val_only\", True)))}',\n"
        "    'trainer.val_before_train=True', 'trainer.resume_mode=disable',\n"
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
        "    args.extend([\n"
        "        'actor_rollout_ref.actor.strategy=fsdp2',\n"
        "        'actor_rollout_ref.actor.fsdp_config.param_offload=True',\n"
        "        'actor_rollout_ref.actor.fsdp_config.optimizer_offload=True',\n"
        "        'actor_rollout_ref.ref.fsdp_config.param_offload=True',\n"
        "    ])\n"
        "if is_async:\n"
        "    args.append('actor_rollout_ref.rollout.mode=async')\n"
        "cmd = ' '.join(shlex.quote(str(item)) for item in args)\n"
        "started = time.monotonic()\n"
        "proc = _run(cmd, env=env, log_path=log_path, timeout_seconds=row_timeout_seconds)\n"
        "elapsed = time.monotonic() - started\n"
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
        "status = 'passed' if proc.returncode == 0 and sample_count > 0 else 'failed'\n"
        "if status == 'passed':\n"
        "    error = None\n"
        "elif proc.returncode == 124:\n"
        "    error = f'verl timeout after {row_timeout_seconds}s; samples={sample_count}'\n"
        "else:\n"
        "    error = f'verl exit={proc.returncode}; samples={sample_count}'\n"
        "result = {\n"
        "    'status': status,\n"
        "    'elapsed_seconds': elapsed,\n"
        "    'tokens_per_second': (sample_count * int(row['output_tokens']) / elapsed) if elapsed > 0 and sample_count else None,\n"
        "    'latency_ms': (elapsed * 1000 / sample_count) if sample_count else None,\n"
        "    'sample_count': sample_count,\n"
        "    'accuracy': accuracy,\n"
        "    'consistency': consistency,\n"
        "    'log_path': str(log_path),\n"
        "    'error': error,\n"
        "}\n"
        "print('VERL_CASE_RESULT=' + json.dumps(result, ensure_ascii=False))\n"
        "PY"
    )
    return script


def _parse_result(stdout: str) -> dict[str, object] | None:
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("VERL_CASE_RESULT="):
            return json.loads(line.split("=", 1)[1])
    return None


def _execution_profile(run_config: VerlCaseRunConfig) -> str:
    profile = str((run_config.extra or {}).get("execution_profile") or "").strip().lower()
    if profile:
        return profile
    if run_config.server.startswith("A3-") and "Qwen3.5" in run_config.config.model_id:
        return "veomni"
    return "fsdp2"
