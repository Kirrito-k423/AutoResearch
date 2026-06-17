"""Tests for Phase 14 Verl formal-case runner boundaries."""
from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone

from workspace_core.config import ServerSpec


case_config = importlib.import_module("workspace-adapter.verl.case_config")
docker = importlib.import_module("workspace-adapter.verl.docker")
data_prep = importlib.import_module("workspace-adapter.verl.data_prep")
provenance = importlib.import_module("workspace-adapter.verl.provenance")
case_runner = importlib.import_module("workspace-adapter.verl.case_runner")


def _run_config():
    config = case_config.VerlCaseConfig()
    return case_config.VerlCaseRunConfig(
        run_id="run123",
        created_at=datetime(2026, 6, 16, 8, 0, tzinfo=timezone.utc),
        server="A2-AK-225",
        config=config,
        matrix=case_config.build_length_matrix(config),
    )


def test_docker_run_command_contains_ascend_mounts_and_proxy():
    command = docker.build_docker_run_command(
        image="quay.io/ascend/verl:test",
        run_id="run123",
        model_mount="/tmp/model path",
        dataset_mount="/tmp/dataset",
        output_mount="/tmp/output",
        source_mounts={"/verl": "/tmp/verl-src"},
        proxy_url="http://127.0.0.1:7890",
    )

    assert "--device=/dev/davinci0" in command
    assert "--device=/dev/davinci7" in command
    assert "--device=/dev/davinci*" not in command
    assert "--device=/dev/davinci_manager" in command
    assert "--device=/dev/devmm_svm" in command
    assert "--device=/dev/hisi_hdc" in command
    assert "--network=host" in command
    assert "--shm-size=64G" in command
    assert "http_proxy=http://127.0.0.1:7890" in command
    assert "https_proxy=http://127.0.0.1:7890" in command
    assert "HTTP_PROXY=http://127.0.0.1:7890" in command
    assert "HTTPS_PROXY=http://127.0.0.1:7890" in command
    assert "all_proxy=http://127.0.0.1:7890" in command
    assert "ALL_PROXY=http://127.0.0.1:7890" in command
    assert "no_proxy=localhost,127.0.0.1,.huawei.com" in command
    assert "NO_PROXY=localhost,127.0.0.1,.huawei.com" in command
    assert "'/tmp/model path':/app/ckpt:ro" in command
    assert "/tmp/verl-src:/verl" in command


def test_docker_run_command_omits_proxy_when_none():
    command = docker.build_docker_run_command(
        image="img",
        run_id="run123",
        model_mount="/m",
        dataset_mount="/d",
        output_mount="/o",
    )

    assert "http_proxy" not in command
    assert "https_proxy" not in command
    assert "HTTP_PROXY" not in command
    assert "HTTPS_PROXY" not in command
    assert "ALL_PROXY" not in command


def test_docker_run_command_allows_smaller_device_count():
    command = docker.build_docker_run_command(
        image="img",
        run_id="run123",
        model_mount="/m",
        dataset_mount="/d",
        output_mount="/o",
        device_count=2,
    )

    assert "--device=/dev/davinci0" in command
    assert "--device=/dev/davinci1" in command
    assert "--device=/dev/davinci2" not in command


def test_prepare_geometry3k_preserves_multimodal_rows(tmp_path):
    fixture = tmp_path / "geometry.jsonl"
    fixture.write_text(
        json.dumps(
            {
                "id": "g1",
                "image": "images/1.png",
                "problem": "Find x.",
                "answer": "42",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    prepared = data_prep.prepare_geometry3k(
        case_config.VerlCaseConfig(),
        tmp_path / "cache",
        local_dataset_path=fixture,
    )

    assert prepared.ready is True
    assert prepared.sample_count == 1
    row = json.loads(prepared.jsonl_path.read_text(encoding="utf-8").strip())
    assert row == {
        "sample_id": "g1",
        "image": "images/1.png",
        "problem": "Find x.",
        "answer": "42",
    }


def test_prepare_geometry3k_rejects_missing_image(tmp_path):
    fixture = tmp_path / "geometry.json"
    fixture.write_text(json.dumps([{"problem": "Find x.", "answer": "42"}]), encoding="utf-8")

    try:
        data_prep.prepare_geometry3k(
            case_config.VerlCaseConfig(),
            tmp_path / "cache",
            local_dataset_path=fixture,
        )
    except data_prep.DataPrepError as exc:
        assert "missing image" in str(exc)
    else:
        raise AssertionError("expected DataPrepError")


def test_capture_repo_provenance_without_push(tmp_path):
    calls = []

    def runner(args, cwd):
        calls.append(args)
        if args[1:] == ["rev-parse", "--show-toplevel"]:
            return 0, str(tmp_path), ""
        if args[1:] == ["remote", "get-url", "origin"]:
            return 0, "https://github.com/upstream/verl.git", ""
        if args[1:] == ["remote", "-v"]:
            return 0, "origin https://github.com/upstream/verl.git (fetch)\norigin https://github.com/upstream/verl.git (push)", ""
        if args[1:] == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return 0, "main", ""
        if args[1:] == ["status", "--porcelain"]:
            return 0, "", ""
        if args[1:] == ["rev-parse", "HEAD"]:
            return 0, "abc123", ""
        return 1, "", "unexpected"

    result = provenance.capture_repo_provenance(
        tmp_path,
        upstream_url="https://github.com/verl-project/verl.git",
        runner=runner,
    )

    assert result.repo == tmp_path.name
    assert result.dirty is False
    assert result.commit_sha == "abc123"
    assert result.fork_url == "https://github.com/Kirrito-k423/verl"
    assert all(args[1] != "push" for args in calls)


def test_capture_repo_provenance_pushes_to_fork_remote(tmp_path):
    calls = []

    def runner(args, cwd):
        calls.append(args)
        if args[1:] == ["rev-parse", "--show-toplevel"]:
            return 0, str(tmp_path), ""
        if args[1:] == ["remote", "get-url", "origin"]:
            return 0, "https://github.com/verl-project/verl.git", ""
        if args[1:] == ["remote", "-v"]:
            return (
                0,
                "\n".join(
                    [
                        "origin https://github.com/verl-project/verl.git (fetch)",
                        "origin https://github.com/verl-project/verl.git (push)",
                        "fork https://github.com/Kirrito-k423/verl.git (fetch)",
                        "fork https://github.com/Kirrito-k423/verl.git (push)",
                    ]
                ),
                "",
            )
        if args[1:] == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return 0, "main", ""
        if args[1:] == ["status", "--porcelain"]:
            return 0, "", ""
        if args[1:] == ["push", "-u", "fork", "main"]:
            return 0, "", ""
        if args[1:] == ["rev-parse", "HEAD"]:
            return 0, "abc123", ""
        return 1, "", "unexpected"

    result = provenance.capture_repo_provenance(
        tmp_path,
        upstream_url="https://github.com/verl-project/verl.git",
        allow_commit_push=True,
        runner=runner,
    )

    assert ["git", "push", "-u", "fork", "main"] in calls
    assert ["git", "push", "-u", "origin", "main"] not in calls
    assert result.pushed_url == "https://github.com/Kirrito-k423/verl/tree/main"
    assert result.branch_url == "https://github.com/Kirrito-k423/verl/tree/main"


def test_capture_repo_provenance_names_detached_head_from_short_sha(tmp_path):
    def runner(args, cwd):
        if args[1:] == ["rev-parse", "--show-toplevel"]:
            return 0, str(tmp_path), ""
        if args[1:] == ["remote", "get-url", "origin"]:
            return 0, "https://github.com/vllm-project/vllm.git", ""
        if args[1:] == ["remote", "-v"]:
            return 0, "origin https://github.com/vllm-project/vllm.git (fetch)\norigin https://github.com/vllm-project/vllm.git (push)", ""
        if args[1:] == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return 0, "HEAD", ""
        if args[1:] == ["rev-parse", "--short", "HEAD"]:
            return 0, "b8b302c", ""
        if args[1:] == ["status", "--porcelain"]:
            return 0, "", ""
        if args[1:] == ["rev-parse", "HEAD"]:
            return 0, "b8b302cde434df8c9289a2b465406b47ebab1c2d", ""
        return 1, "", "unexpected"

    result = provenance.capture_repo_provenance(
        tmp_path,
        upstream_url="https://github.com/vllm-project/vllm.git",
        runner=runner,
    )

    assert result.branch == "detached-b8b302c"
    assert result.branch_url == "https://github.com/Kirrito-k423/vllm/tree/detached-b8b302c"


def test_capture_repo_provenance_strips_old_verl_case_prefix_from_branch_seed(tmp_path):
    calls = []

    def runner(args, cwd):
        calls.append(args)
        if args[1:] == ["rev-parse", "--show-toplevel"]:
            return 0, str(tmp_path), ""
        if args[1:] == ["remote", "get-url", "origin"]:
            return 0, "https://github.com/Kirrito-k423/AutoResearch.git", ""
        if args[1:] == ["remote", "-v"]:
            return 0, "origin https://github.com/Kirrito-k423/AutoResearch.git (fetch)\norigin https://github.com/Kirrito-k423/AutoResearch.git (push)", ""
        if args[1:] == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return 0, "codex/verl-case-OLDRUNID-codex/phase-02-workspace-core", ""
        if args[1:] == ["status", "--porcelain"]:
            return 0, "", ""
        if args[1:] == ["switch", "-C", "codex/verl-case-NEWRUNID-phase-02-workspace-core"]:
            return 0, "", ""
        if args[1:] == ["push", "-u", "origin", "codex/verl-case-NEWRUNID-phase-02-workspace-core"]:
            return 0, "", ""
        if args[1:] == ["rev-parse", "HEAD"]:
            return 0, "abc123", ""
        return 1, "", "unexpected"

    result = provenance.capture_repo_provenance(
        tmp_path,
        allow_commit_push=True,
        branch_prefix="codex/verl-case-NEWRUNID-",
        runner=runner,
    )

    assert result.branch == "codex/verl-case-NEWRUNID-phase-02-workspace-core"
    assert ["git", "switch", "-C", "codex/verl-case-NEWRUNID-phase-02-workspace-core"] in calls


def test_run_verl_case_fails_if_one_matrix_row_fails():
    run_config = _run_config()
    calls = []

    def runner(spec, command, timeout):
        calls.append(command)
        if command.startswith("docker image inspect"):
            return 1, "", "missing"
        if command.startswith("docker pull"):
            return 0, "pulled", ""
        if "async-1024-16384" in command:
            return 1, "", "oom"
        payload = {
            "status": "passed",
            "elapsed_seconds": 1.0,
            "tokens_per_second": 2.0,
            "latency_ms": 500.0,
            "sample_count": 1,
            "accuracy": 1.0,
            "consistency": 1.0,
        }
        return 0, "VERL_CASE_RESULT=" + json.dumps(payload), ""

    result = case_runner.run_verl_case(
        ServerSpec(name="A2-AK-225", host="h", user="root"),
        run_config,
        timeout=1.0,
        runner=runner,
    )

    assert calls[0].startswith("docker image inspect")
    assert calls[1].startswith("docker pull")
    assert result.ok is False
    assert any(row.status == "failed" and row.output_tokens == 16384 for row in result.rows)


def test_run_verl_case_passes_all_rows_and_script_contains_ignore_eos_false():
    run_config = _run_config()

    def runner(spec, command, timeout):
        if command.startswith("docker image inspect"):
            return 1, "", "missing"
        if command.startswith("docker pull"):
            return 0, "pulled", ""
        payload = {
            "status": "passed",
            "elapsed_seconds": 1.0,
            "tokens_per_second": 2.0,
            "latency_ms": 500.0,
            "sample_count": 1,
            "accuracy": 1.0,
            "consistency": 1.0,
        }
        return 0, "VERL_CASE_RESULT=" + json.dumps(payload), ""

    result = case_runner.run_verl_case(
        ServerSpec(name="A2-AK-225", host="h", user="root"),
        run_config,
        timeout=1.0,
        runner=runner,
    )

    assert result.ok is True
    assert len(result.rows) == 8
    assert '"ignore_eos": false' in case_runner.build_remote_case_script(run_config)


def test_run_verl_case_mounts_staged_dependency_sources():
    run_config = _run_config()
    run_config.config.dependency_repo_paths = {"verl": "/Users/Zhuanz/work/github/verl"}
    calls = []

    def source_syncer(spec, config):
        assert config.run_id == "run123"
        return {"/verl": "/remote/deps/verl"}

    def runner(spec, command, timeout):
        calls.append(command)
        if command.startswith("docker image inspect"):
            return 0, "", ""
        payload = {
            "status": "passed",
            "elapsed_seconds": 1.0,
            "tokens_per_second": 2.0,
            "latency_ms": 500.0,
            "sample_count": 1,
            "accuracy": 1.0,
            "consistency": 1.0,
        }
        return 0, "VERL_CASE_RESULT=" + json.dumps(payload), ""

    result = case_runner.run_verl_case(
        ServerSpec(name="A3-AX-180", host="h", user="root"),
        run_config,
        timeout=1.0,
        runner=runner,
        source_syncer=source_syncer,
    )

    assert result.ok is True
    docker_runs = [command for command in calls if command.startswith("docker run")]
    assert docker_runs
    assert any("/remote/deps/verl:/verl" in command for command in docker_runs)


def test_run_verl_case_surfaces_dependency_sync_errors():
    run_config = _run_config()

    def source_syncer(spec, config):
        raise case_runner.DependencySourceSyncError("sync failed")

    result = case_runner.run_verl_case(
        ServerSpec(name="A3-AX-180", host="h", user="root"),
        run_config,
        timeout=1.0,
        source_syncer=source_syncer,
    )

    assert result.ok is False
    assert result.rows == []
    assert result.error == "sync failed"


def test_run_verl_case_skips_pull_when_image_already_exists():
    run_config = _run_config()
    calls = []

    def runner(spec, command, timeout):
        calls.append(command)
        if command.startswith("docker image inspect"):
            return 0, "", ""
        if command.startswith("docker pull"):
            raise AssertionError("docker pull should be skipped when image already exists")
        payload = {
            "status": "passed",
            "elapsed_seconds": 1.0,
            "tokens_per_second": 2.0,
            "latency_ms": 500.0,
            "sample_count": 1,
            "accuracy": 1.0,
            "consistency": 1.0,
        }
        return 0, "VERL_CASE_RESULT=" + json.dumps(payload), ""

    result = case_runner.run_verl_case(
        ServerSpec(name="A3-AX-180", host="h", user="root"),
        run_config,
        timeout=1.0,
        runner=runner,
    )

    assert calls[0].startswith("docker image inspect")
    assert all(not command.startswith("docker pull") for command in calls)
    assert result.ok is True


def test_row_command_builds_formal_verl_script():
    command = case_runner._row_command(_run_config(), "sync-1024-2048")
    async_command = case_runner._row_command(_run_config(), "async-1024-2048")

    assert "verl.trainer.main_ppo" in command
    assert "examples/data_preprocess/geo3k.py" in command
    assert "algorithm.adv_estimator=grpo" in command
    assert "actor_rollout_ref.rollout.mode=sync" not in command
    assert "actor_rollout_ref.rollout.mode=async" in async_command
    assert "actor_rollout_ref.rollout.ignore_eos=False" in command
    assert "actor_rollout_ref.actor.strategy=fsdp2" in command
    assert "trainer.balance_batch=True" in command
    assert "data.return_raw_chat=True" in command
    assert "WANDB_DIR" in command
    assert "trainer.logger=[console,wandb]" in command
    assert "row_timeout_seconds" in command
    assert "VERL_CASE_RESULT=" in command
