"""Tests for Phase 14 Verl formal-case runner boundaries."""
from __future__ import annotations

import importlib
import json
import sys
import types
from datetime import datetime, timezone
from pathlib import Path

from workspace_core.config import ServerSpec


case_config = importlib.import_module("workspace-adapter.verl.case_config")
docker = importlib.import_module("workspace-adapter.verl.docker")
data_prep = importlib.import_module("workspace-adapter.verl.data_prep")
model_sync = importlib.import_module("workspace-adapter.verl.model_sync")
provenance = importlib.import_module("workspace-adapter.verl.provenance")
case_runner = importlib.import_module("workspace-adapter.verl.case_runner")
source_sync = importlib.import_module("workspace-adapter.verl.source_sync")


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


def test_docker_pull_command_includes_proxy_env_when_configured():
    command = docker.build_docker_pull_command(
        "quay.io/ascend/verl:test",
        proxy_url="http://127.0.0.1:17895",
    )

    assert command.startswith("env ")
    assert "http_proxy=http://127.0.0.1:17895" in command
    assert "https_proxy=http://127.0.0.1:17895" in command
    assert "ALL_PROXY=http://127.0.0.1:17895" in command
    assert command.endswith("docker pull quay.io/ascend/verl:test")


def test_docker_exec_command_wraps_shell_command():
    command = docker.build_docker_exec_command(
        container_name="verl-8.5.2-a2",
        command="/bin/bash -lc 'echo ok'",
    )

    assert command == "docker exec -i verl-8.5.2-a2 /bin/bash -lc 'echo ok'"


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


def test_prepare_geometry3k_detects_existing_parquet_cache(tmp_path):
    dataset_cache = tmp_path / "cache" / "datasets" / "hiyouga__geometry3k"
    dataset_cache.mkdir(parents=True)
    (dataset_cache / "train.parquet").write_bytes(b"train")
    (dataset_cache / "test.parquet").write_bytes(b"test")

    prepared = data_prep.prepare_geometry3k(
        case_config.VerlCaseConfig(),
        tmp_path / "cache",
    )

    assert prepared.ready is True
    assert prepared.train_parquet == dataset_cache / "train.parquet"
    assert prepared.test_parquet == dataset_cache / "test.parquet"


def test_stage_geometry3k_uploads_cached_parquet(tmp_path, monkeypatch):
    dataset_cache = tmp_path / "cache" / "datasets" / "hiyouga__geometry3k"
    dataset_cache.mkdir(parents=True)
    (dataset_cache / "train.parquet").write_bytes(b"train")
    (dataset_cache / "test.parquet").write_bytes(b"test")
    prepared = data_prep.prepare_geometry3k(
        case_config.VerlCaseConfig(),
        tmp_path / "cache",
    )
    mkdir_calls = []
    put_calls = []

    class _SFTP:
        def put(self, local_path, remote_path):
            put_calls.append((local_path, remote_path))

        def close(self):
            return None

    class _Client:
        def __init__(self, host, bootstrap_password=None):
            self.host = host
            self.bootstrap_password = bootstrap_password

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def exec(self, command, timeout):
            mkdir_calls.append((command, timeout))
            return 0, "", ""

        def sftp(self):
            return _SFTP()

    monkeypatch.setattr(data_prep, "SSHClient", _Client)

    remote_root = data_prep.stage_geometry3k(
        ServerSpec(name="A2-AK-225", host="192.168.9.225", user="root"),
        prepared,
        remote_dataset_dir="/home/t00906153/autoresearch/dataset",
    )

    assert remote_root == "/home/t00906153/autoresearch/dataset"
    assert mkdir_calls == [("mkdir -p /home/t00906153/autoresearch/dataset/geo3k", 30.0)]
    assert put_calls == [
        (str(dataset_cache / "train.parquet"), "/home/t00906153/autoresearch/dataset/geo3k/train.parquet"),
        (str(dataset_cache / "test.parquet"), "/home/t00906153/autoresearch/dataset/geo3k/test.parquet"),
    ]


def test_prepare_model_cache_short_circuits_existing_snapshot(tmp_path):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    (model_cache / "config.json").write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    (model_cache / "model.safetensors-00001-of-00001.safetensors").write_bytes(b"stub")

    prepared = model_sync.prepare_model_cache(
        case_config.VerlCaseConfig(),
        tmp_path / "cache",
    )

    assert prepared.ready is True
    assert prepared.downloaded is False
    assert prepared.model_cache == model_cache


def test_prepare_model_cache_recovers_completed_snapshot_via_resume(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )

    fake_hf = types.ModuleType("huggingface_hub")
    fake_hf.snapshot_download = lambda **kwargs: None
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hf)

    def fake_resume(model_id, cache, *, proxy_url):
        assert model_id == "Qwen/Qwen3.5-2B"
        assert cache == model_cache
        assert proxy_url is None
        (cache / "model.safetensors-00001-of-00001.safetensors").write_bytes(b"stub")

    monkeypatch.setattr(model_sync, "_resume_model_download", fake_resume)

    prepared = model_sync.prepare_model_cache(
        case_config.VerlCaseConfig(),
        tmp_path / "cache",
    )

    assert prepared.ready is True
    assert prepared.downloaded is True
    assert prepared.model_cache == model_cache


def test_prepare_model_cache_prefers_existing_incomplete_resume(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "generation_config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    download_dir = model_cache / ".cache" / "huggingface" / "download"
    download_dir.mkdir(parents=True)
    (download_dir / "largest.incomplete").write_bytes(b"abc")

    fake_hf = types.ModuleType("huggingface_hub")

    def fake_snapshot_download(**kwargs):
        raise AssertionError("snapshot_download should not run when resumable cache exists")

    fake_hf.snapshot_download = fake_snapshot_download
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hf)

    def fake_resume(model_id, cache, *, proxy_url):
        assert model_id == "Qwen/Qwen3.5-2B"
        assert cache == model_cache
        assert proxy_url == "http://127.0.0.1:7890"
        (cache / "model.safetensors-00001-of-00001.safetensors").write_bytes(b"stub")

    monkeypatch.setattr(model_sync, "_resume_model_download", fake_resume)

    prepared = model_sync.prepare_model_cache(
        case_config.VerlCaseConfig(),
        tmp_path / "cache",
        proxy_url="http://127.0.0.1:7890",
    )

    assert prepared.ready is True
    assert prepared.downloaded is True
    assert prepared.model_cache == model_cache


def test_stage_model_cache_reuses_shared_remote_cache(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    (model_cache / "config.json").write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    (model_cache / "model.safetensors-00001-of-00001.safetensors").write_bytes(b"stub")

    exec_calls = []
    put_calls = []

    class _SFTP:
        def put(self, local_path, remote_path):
            put_calls.append((local_path, remote_path))

        def close(self):
            return None

    class _Client:
        def __init__(self, host, bootstrap_password=None):
            self.host = host
            self.bootstrap_password = bootstrap_password

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def exec(self, command, timeout):
            exec_calls.append(command)
            if "/home/t00906153/autoresearch/model-cache/Qwen__Qwen3.5-2B/config.json" in command:
                return 0, "", ""
            raise AssertionError(f"unexpected exec command: {command}")

        def sftp(self):
            return _SFTP()

    monkeypatch.setattr(model_sync, "SSHClient", _Client)

    remote_path = model_sync.stage_model_cache(
        ServerSpec(name="A3-AX-180", host="192.168.13.180", user="root"),
        local_model_dir=model_cache,
        remote_model_dir="/home/t00906153/autoresearch/runs/run123/model",
        remote_shared_model_root="/home/t00906153/autoresearch/model-cache",
    )

    assert remote_path == "/home/t00906153/autoresearch/model-cache/Qwen__Qwen3.5-2B"
    assert put_calls == []
    assert len(exec_calls) == 1


def test_source_sync_maps_transformers_package_dir_to_src_mount(tmp_path):
    package_dir = tmp_path / "transformers"
    (package_dir / "utils").mkdir(parents=True)
    (package_dir / "utils" / "generic.py").write_text("# stub\n", encoding="utf-8")

    repo_dir = tmp_path / "transformers-repo"
    (repo_dir / "src" / "transformers" / "utils").mkdir(parents=True)
    (repo_dir / "src" / "transformers" / "utils" / "generic.py").write_text("# stub\n", encoding="utf-8")

    assert source_sync._container_mount_path("transformers", package_dir) == "/transformers/src/transformers"
    assert source_sync._container_mount_path("transformers", repo_dir) == "/transformers"


def test_source_sync_filters_local_vllm_for_veomni_profile():
    filtered = source_sync.filter_dependency_repo_paths(
        dependency_repo_paths={
            "verl": "/tmp/verl",
            "vllm": "/tmp/vllm",
            "veomni": "/tmp/veomni",
            "transformers": "/tmp/transformers",
        },
        server="A3-AX-180",
        model_id="Qwen/Qwen3.5-2B",
    )

    assert filtered == {
        "verl": "/tmp/verl",
        "veomni": "/tmp/veomni",
        "transformers": "/tmp/transformers",
    }


def test_default_source_syncer_skips_local_vllm_for_veomni(monkeypatch):
    run_config = case_config.VerlCaseRunConfig(
        run_id="run123",
        created_at=datetime(2026, 6, 16, 8, 0, tzinfo=timezone.utc),
        server="A3-AX-180",
        config=case_config.VerlCaseConfig(
            dependency_repo_paths={
                "verl": "/tmp/verl",
                "vllm": "/tmp/vllm",
                "veomni": "/tmp/veomni",
            }
        ),
        matrix=case_config.build_length_matrix(case_config.VerlCaseConfig()),
    )
    captured = {}

    def fake_stage_dependency_sources(spec, *, run_id, remote_workdir, dependency_repo_paths):
        captured["run_id"] = run_id
        captured["remote_workdir"] = remote_workdir
        captured["dependency_repo_paths"] = dependency_repo_paths
        return {}

    monkeypatch.setattr(case_runner, "stage_dependency_sources", fake_stage_dependency_sources)

    result = case_runner._default_source_syncer(
        ServerSpec(name="A3-AX-180", host="192.168.13.180", user="root"),
        run_config,
    )

    assert result == {}
    assert captured["run_id"] == "run123"
    assert "vllm" not in captured["dependency_repo_paths"]
    assert captured["dependency_repo_paths"]["verl"] == "/tmp/verl"
    assert captured["dependency_repo_paths"]["veomni"] == "/tmp/veomni"


def test_resume_model_download_continues_largest_incomplete(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "generation_config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    download_dir = model_cache / ".cache" / "huggingface" / "download"
    download_dir.mkdir(parents=True)
    largest = download_dir / "largest.incomplete"
    largest.write_bytes(b"abc")
    (download_dir / "smaller.incomplete").write_bytes(b"a")

    class _Response:
        def __init__(self, *, status_code=200, headers=None, chunks=None):
            self.status_code = status_code
            self.headers = headers or {}
            self._chunks = chunks or []

        def raise_for_status(self):
            return None

        def iter_content(self, chunk_size=0):
            yield from self._chunks

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class _Session:
        def get(self, url, **kwargs):
            if kwargs.get("allow_redirects") is False:
                return _Response(
                    status_code=302,
                    headers={
                        "location": "https://example.com/model.safetensors-00001-of-00001.safetensors",
                        "x-linked-size": "6",
                    },
                )
            assert kwargs["headers"]["Range"] == "bytes=3-"
            return _Response(status_code=206, chunks=[b"def"])

    monkeypatch.setattr(model_sync.requests, "Session", lambda: _Session())

    model_sync._resume_model_download(
        "Qwen/Qwen3.5-2B",
        model_cache,
        proxy_url=None,
    )

    assert (model_cache / "model.safetensors-00001-of-00001.safetensors").read_bytes() == b"abcdef"
    assert not largest.exists()


def test_resume_model_download_retries_after_stream_break(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "generation_config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    download_dir = model_cache / ".cache" / "huggingface" / "download"
    download_dir.mkdir(parents=True)
    largest = download_dir / "largest.incomplete"
    largest.write_bytes(b"abc")

    class _Response:
        def __init__(self, *, status_code=206, chunks=None, error=None):
            self.status_code = status_code
            self.headers = {}
            self._chunks = chunks or []
            self._error = error

        def raise_for_status(self):
            return None

        def iter_content(self, chunk_size=0):
            for chunk in self._chunks:
                yield chunk
            if self._error is not None:
                raise self._error

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class _Session:
        def __init__(self):
            self.calls = 0

        def get(self, url, **kwargs):
            self.calls += 1
            if kwargs.get("allow_redirects") is False:
                return _Response(status_code=302)
            range_header = kwargs["headers"]["Range"]
            if range_header == "bytes=3-":
                return _Response(
                    chunks=[b"de"],
                    error=model_sync.requests.exceptions.ChunkedEncodingError("broken"),
                )
            assert range_header == "bytes=5-"
            return _Response(chunks=[b"f"])

    monkeypatch.setattr(model_sync.requests, "Session", lambda: _Session())
    monkeypatch.setattr(
        model_sync,
        "_resolve_download_url",
        lambda session, resolve_url, proxies: ("https://example.com/model.safetensors-00001-of-00001.safetensors", 6),
    )

    model_sync._resume_model_download(
        "Qwen/Qwen3.5-2B",
        model_cache,
        proxy_url=None,
    )

    assert (model_cache / "model.safetensors-00001-of-00001.safetensors").read_bytes() == b"abcdef"
    assert not largest.exists()


def test_resume_model_download_prefers_curl_with_proxy(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "generation_config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    download_dir = model_cache / ".cache" / "huggingface" / "download"
    download_dir.mkdir(parents=True)
    largest = download_dir / "largest.incomplete"
    largest.write_bytes(b"abc")

    def fake_curl_resume(*, resolve_url, incomplete_path, proxy_url, expected_size):
        assert resolve_url.endswith("model.safetensors-00001-of-00001.safetensors")
        assert incomplete_path.read_bytes() == b"abc"
        assert proxy_url == "http://127.0.0.1:7890"
        assert expected_size == 6
        incomplete_path.write_bytes(b"abcdef")

    monkeypatch.setattr(model_sync, "_resolve_expected_size_via_curl", lambda **kwargs: 6)
    monkeypatch.setattr(model_sync, "_resume_via_curl", fake_curl_resume)

    model_sync._resume_model_download(
        "Qwen/Qwen3.5-2B",
        model_cache,
        proxy_url="http://127.0.0.1:7890",
    )

    assert (model_cache / "model.safetensors-00001-of-00001.safetensors").read_bytes() == b"abcdef"
    assert not largest.exists()


def test_resume_model_download_prefers_parallel_curl_for_large_proxy_resume(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "generation_config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    download_dir = model_cache / ".cache" / "huggingface" / "download"
    download_dir.mkdir(parents=True)
    largest = download_dir / "largest.incomplete"
    largest.write_bytes(b"abc")

    def fake_parallel_resume(*, resolve_url, incomplete_path, proxy_url, expected_size):
        assert resolve_url.endswith("model.safetensors-00001-of-00001.safetensors")
        assert incomplete_path.read_bytes() == b"abc"
        assert proxy_url == "http://127.0.0.1:7890"
        assert expected_size == 10
        incomplete_path.write_bytes(b"abcdefghij")

    monkeypatch.setattr(model_sync, "_resolve_expected_size_via_curl", lambda **kwargs: 10)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_THRESHOLD_BYTES", 4)
    monkeypatch.setattr(model_sync, "_resume_via_parallel_curl", fake_parallel_resume)

    model_sync._resume_model_download(
        "Qwen/Qwen3.5-2B",
        model_cache,
        proxy_url="http://127.0.0.1:7890",
    )

    assert (model_cache / "model.safetensors-00001-of-00001.safetensors").read_bytes() == b"abcdefghij"
    assert not largest.exists()


def test_resolve_expected_size_via_curl_reads_last_content_length(monkeypatch):
    class _Proc:
        returncode = 0
        stdout = (
            "HTTP/2 302\n"
            "content-length: 1066\n"
            "x-linked-size: 4548221488\n"
        )
        stderr = ""

    monkeypatch.setattr(model_sync.subprocess, "run", lambda *args, **kwargs: _Proc())

    size = model_sync._resolve_expected_size_via_curl(
        resolve_url="https://huggingface.co/Qwen/Qwen3.5-2B/resolve/main/model.safetensors-00001-of-00001.safetensors",
        proxy_url="http://127.0.0.1:7890",
    )

    assert size == 4548221488


def test_resume_model_download_uses_cached_expected_size_for_proxy(tmp_path, monkeypatch):
    model_cache = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_cache.mkdir(parents=True)
    for name in (
        "chat_template.json",
        "config.json",
        "generation_config.json",
        "merges.txt",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "video_preprocessor_config.json",
        "vocab.json",
    ):
        (model_cache / name).write_text("{}", encoding="utf-8")
    (model_cache / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    download_dir = model_cache / ".cache" / "huggingface" / "download"
    download_dir.mkdir(parents=True)
    largest = download_dir / "largest.incomplete"
    largest.write_bytes(b"abc")
    model_sync._write_cached_expected_size(largest, 6)

    def fail_resolve(**kwargs):
        raise AssertionError("size resolver should not run when cache exists")

    def fake_curl_resume(*, resolve_url, incomplete_path, proxy_url, expected_size):
        assert expected_size == 6
        incomplete_path.write_bytes(b"abcdef")

    monkeypatch.setattr(model_sync, "_resolve_expected_size_via_curl", fail_resolve)
    monkeypatch.setattr(model_sync, "_resume_via_curl", fake_curl_resume)

    model_sync._resume_model_download(
        "Qwen/Qwen3.5-2B",
        model_cache,
        proxy_url="http://127.0.0.1:7890",
    )

    assert (model_cache / "model.safetensors-00001-of-00001.safetensors").read_bytes() == b"abcdef"
    assert not largest.exists()


def test_resume_via_parallel_curl_appends_parts_in_order(tmp_path, monkeypatch):
    incomplete = tmp_path / "largest.incomplete"
    incomplete.write_bytes(b"abc")
    calls = []

    class _Proc:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(command, text, capture_output, check):
        calls.append(command)
        range_value = command[command.index("--range") + 1]
        output_path = Path(command[command.index("--output") + 1])
        start, end = [int(part) for part in range_value.split("-", 1)]
        part_index = len(calls) - 1
        output_path.write_bytes(bytes([65 + part_index]) * (end - start + 1))
        return _Proc()

    monkeypatch.setattr(model_sync.subprocess, "run", fake_run)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_WORKERS", 2)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_THRESHOLD_BYTES", 2)

    model_sync._resume_via_parallel_curl(
        resolve_url="https://example.com/model",
        incomplete_path=incomplete,
        proxy_url="http://127.0.0.1:7890",
        expected_size=7,
    )

    assert incomplete.read_bytes() == b"abcAABB"
    assert any("--range" in command for command in calls)


def test_resume_via_parallel_curl_reuses_existing_partial_parts(tmp_path, monkeypatch):
    incomplete = tmp_path / "largest.incomplete"
    incomplete.write_bytes(b"abc")
    part_dir = tmp_path / "largest.incomplete.parts"
    part_dir.mkdir()
    (part_dir / "part-00.bin").write_bytes(b"A")
    calls = []

    class _Proc:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(command, text, capture_output, check):
        calls.append(command)
        range_value = command[command.index("--range") + 1]
        output_path = Path(command[command.index("--output") + 1])
        start, end = [int(part) for part in range_value.split("-", 1)]
        output_path.write_bytes(b"Z" * (end - start + 1))
        return _Proc()

    monkeypatch.setattr(model_sync.subprocess, "run", fake_run)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_WORKERS", 2)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_THRESHOLD_BYTES", 2)

    model_sync._resume_via_parallel_curl(
        resolve_url="https://example.com/model",
        incomplete_path=incomplete,
        proxy_url="http://127.0.0.1:7890",
        expected_size=7,
    )

    assert incomplete.read_bytes() == b"abcAZZZ"
    assert sorted(command[command.index("--range") + 1] for command in calls) == ["4-4", "5-6"]
    assert not part_dir.exists()


def test_resume_via_parallel_curl_recovers_temp_partial_before_resuming(tmp_path, monkeypatch):
    incomplete = tmp_path / "largest.incomplete"
    incomplete.write_bytes(b"abc")
    part_dir = tmp_path / "largest.incomplete.parts"
    part_dir.mkdir()
    (part_dir / "part-00.bin").write_bytes(b"A")
    (part_dir / "part-00.bin.partial").write_bytes(b"B")
    calls = []

    class _Proc:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(command, text, capture_output, check):
        calls.append(command)
        range_value = command[command.index("--range") + 1]
        output_path = Path(command[command.index("--output") + 1])
        start, end = [int(part) for part in range_value.split("-", 1)]
        output_path.write_bytes(b"Z" * (end - start + 1))
        return _Proc()

    monkeypatch.setattr(model_sync.subprocess, "run", fake_run)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_WORKERS", 2)
    monkeypatch.setattr(model_sync, "PARALLEL_CURL_THRESHOLD_BYTES", 2)

    model_sync._resume_via_parallel_curl(
        resolve_url="https://example.com/model",
        incomplete_path=incomplete,
        proxy_url="http://127.0.0.1:7890",
        expected_size=7,
    )

    assert incomplete.read_bytes() == b"abcABZZ"
    assert sorted(command[command.index("--range") + 1] for command in calls) == ["5-6"]
    assert not part_dir.exists()


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
        if "docker pull" in command:
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
    assert "docker pull" in calls[1]
    assert result.ok is False
    assert any(row.status == "failed" and row.output_tokens == 16384 for row in result.rows)


def test_run_verl_case_passes_all_rows_and_script_contains_ignore_eos_false():
    run_config = _run_config()

    def runner(spec, command, timeout):
        if command.startswith("docker image inspect"):
            return 1, "", "missing"
        if "docker pull" in command:
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
    run_config.config.dependency_repo_paths = {
        "verl": "/Users/Zhuanz/work/github/verl",
        "veomni": "/Users/Zhuanz/work/test/ut-addition/repos/VeOmni",
    }
    calls = []

    def source_syncer(spec, config):
        assert config.run_id == "run123"
        return {
            "/verl": "/remote/deps/verl",
            "/veomni": "/remote/deps/veomni",
        }

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
    assert any("/remote/deps/veomni:/veomni" in command for command in docker_runs)


def test_run_verl_case_reuses_matching_running_container():
    run_config = _run_config()
    run_config.config.dependency_repo_paths = {"verl": "/Users/Zhuanz/work/github/verl"}
    calls = []

    def source_syncer(spec, config):
        return {"/verl": "/home/t00906153/autoresearch/runs/run123/deps/verl"}

    def runner(spec, command, timeout):
        calls.append(command)
        if command.startswith("docker image inspect"):
            return 0, "", ""
        if command.startswith("docker ps --filter status=running"):
            return 0, "verl-8.5.2-a2\n", ""
        if "ps -eo args=" in command:
            return 0, "", ""
        if "AR_FORMAL_SMOKE_OK=1" in command:
            return 0, "AR_FORMAL_SMOKE_OK=1\nAR_FORMAL_SMOKE_VALUE=[1.0]\n", ""
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
        source_syncer=source_syncer,
    )

    assert result.ok is True
    assert all(not command.startswith("docker run") for command in calls)
    exec_calls = [command for command in calls if command.startswith("docker exec -i verl-8.5.2-a2")]
    assert exec_calls
    assert any("/home/t00906153/autoresearch/runs/run123/deps/verl" in command for command in exec_calls)


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
        if "docker pull" in command:
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
    assert all("docker pull" not in command for command in calls)
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
    assert "trainer.device=npu" in command
    assert "data.return_raw_chat=True" in command


def test_row_command_uses_custom_exec_paths():
    command = case_runner._row_command(
        _run_config(),
        "sync-1024-2048",
        paths={
            "verl_root": "/home/t00906153/autoresearch/runs/run123/deps/verl",
            "model_root": "/home/t00906153/autoresearch/runs/run123/model",
            "dataset_root": "/home/t00906153/autoresearch/dataset",
            "output_root": "/home/t00906153/autoresearch/runs/run123",
        },
    )

    assert "/home/t00906153/autoresearch/runs/run123/deps/verl" in command
    assert "/home/t00906153/autoresearch/runs/run123/model" in command
    assert "/home/t00906153/autoresearch/dataset" in command
    assert "PYTHONUNBUFFERED" in command
    assert "RAY_EXPERIMENTAL_NOSET_ASCEND_RT_VISIBLE_DEVICES" in command
    assert "ASCEND_RT_VISIBLE_DEVICES" in command
    assert "HCCL_CONNECT_TIMEOUT" in command
    assert "WANDB_DIR" in command


def test_row_command_uses_veomni_profile_for_a3_qwen35():
    config = case_config.VerlCaseConfig()
    run_config = case_config.VerlCaseRunConfig(
        run_id="run123",
        created_at=datetime(2026, 6, 16, 8, 0, tzinfo=timezone.utc),
        server="A3-AX-180",
        config=config,
        matrix=case_config.build_length_matrix(config),
    )

    command = case_runner._row_command(run_config, "sync-1024-2048")

    assert case_runner._execution_profile(run_config) == "veomni"
    assert "model_engine=veomni" in command
    assert "actor_rollout_ref.actor.veomni.param_offload=True" in command
    assert "actor_rollout_ref.ref.veomni.param_offload=True" in command
    assert "veomni_init_device =" in command
    assert "n_gpus > 1 else" in command
    assert "actor_rollout_ref.actor.veomni.init_device={veomni_init_device}" in command
    assert "actor_rollout_ref.ref.veomni.init_device={veomni_init_device}" in command
    assert "actor_rollout_ref.actor.veomni.rms_norm_gated_implementation=eager" in command
    assert "actor_rollout_ref.actor.veomni.causal_conv1d_implementation=eager" in command
    assert "actor_rollout_ref.actor.veomni.chunk_gated_delta_rule_implementation=eager" in command
    assert "actor_rollout_ref.rollout.data_parallel_size={rollout_data_parallel_size}" in command
    assert "trainer.logger=[console,wandb]" in command
    assert "trainer.use_legacy_worker_impl=disable" in command
    assert "/veomni" in command
    assert "PYTHONPATH" in command
    assert "row_timeout_seconds" in command
    assert "VERL_CASE_RESULT=" in command


def test_row_command_uses_npu_init_device_for_single_gpu_veomni():
    config = case_config.VerlCaseConfig(n_gpus_per_node=1, tensor_model_parallel_size=1)
    run_config = case_config.VerlCaseRunConfig(
        run_id="run123",
        created_at=datetime(2026, 6, 16, 8, 0, tzinfo=timezone.utc),
        server="A3-AX-180",
        config=config,
        matrix=case_config.build_length_matrix(config),
    )

    command = case_runner._row_command(run_config, "sync-1024-2048")

    assert case_runner._execution_profile(run_config) == "veomni"
    assert "veomni_init_device =" in command
    assert "n_gpus > 1 else" in command
    assert "actor_rollout_ref.actor.veomni.init_device={veomni_init_device}" in command
    assert "actor_rollout_ref.ref.veomni.init_device={veomni_init_device}" in command
