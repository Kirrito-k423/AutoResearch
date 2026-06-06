"""Tests for layout paths (D-17, CORE-LAYOUT-01)."""
import pytest

from workspace_core.layout import ensure_run_dir, run_dir, clean_run, ensure_root
from workspace_core.layout.paths import (
    RUNS_DIR, LOGS_DIR, CACHE_DIR, SSH_KEYS_DIR, ROOT_DIR,
    RunIDError, _validate_run_id, RunPaths,
)
import workspace_core.layout.paths as layout_paths


@pytest.fixture
def fake_home(monkeypatch, tmp_path):
    """重定向 ~/.autoresearch → tmp_path/.autoresearch (避免污染真实 home)."""
    fake = tmp_path / ".autoresearch"
    monkeypatch.setattr(layout_paths, "ROOT_DIR", fake)
    monkeypatch.setattr(layout_paths, "RUNS_DIR", fake / "runs")
    monkeypatch.setattr(layout_paths, "LOGS_DIR", fake / "logs")
    monkeypatch.setattr(layout_paths, "CACHE_DIR", fake / "cache")
    monkeypatch.setattr(layout_paths, "SSH_KEYS_DIR", fake / "ssh_keys")
    yield fake


def test_ensure_run_dir_creates_subdirs(fake_home):
    p = ensure_run_dir("2026-06-06-test-001")
    assert p.logs.exists()
    assert p.wandb.exists()
    assert p.prom.exists()
    assert not p.manifest.exists()  # manifest 写到调用方负责


def test_ensure_run_dir_returns_runpaths(fake_home):
    p = ensure_run_dir("smoke-001")
    assert isinstance(p, RunPaths)
    assert p.run_id == "smoke-001"
    assert p.root == fake_home / "runs" / "smoke-001"


def test_ensure_run_dir_conflict_raises(fake_home):
    ensure_run_dir("dup")
    with pytest.raises(FileExistsError) as exc:
        ensure_run_dir("dup")
    assert "已存在" in str(exc.value)


def test_run_dir_no_create(fake_home):
    p = run_dir("lazy", create=False)
    assert not p.logs.exists()
    assert p.run_id == "lazy"


def test_run_id_validation_rejects_path_traversal():
    with pytest.raises(RunIDError):
        _validate_run_id("../etc/passwd")
    with pytest.raises(RunIDError):
        _validate_run_id("a/b")
    with pytest.raises(RunIDError):
        _validate_run_id("")
    with pytest.raises(RunIDError):
        _validate_run_id("a" * 200)  # too long
    with pytest.raises(RunIDError):
        _validate_run_id("-leading-dash")


def test_run_id_validation_accepts_normal():
    assert _validate_run_id("2026-06-06-smoke-001") == "2026-06-06-smoke-001"
    assert _validate_run_id("my_exp.v2") == "my_exp.v2"
    assert _validate_run_id("a") == "a"
    assert _validate_run_id("0123") == "0123"


def test_ensure_root_creates_all_4_dirs(fake_home):
    ensure_root()
    assert (fake_home / "runs").exists()
    assert (fake_home / "logs").exists()
    assert (fake_home / "cache").exists()
    assert (fake_home / "ssh_keys").exists()


def test_clean_run_removes_directory(fake_home):
    p = ensure_run_dir("to-clean")
    assert p.root.exists()
    clean_run("to-clean")
    assert not p.root.exists()
