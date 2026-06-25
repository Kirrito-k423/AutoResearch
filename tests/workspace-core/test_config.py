"""Tests for config loader (D-10..13)."""
import os
import pytest

from workspace_core.config import from_yaml, from_path, ConfigError


def test_from_yaml_minimal():
    cfg = from_yaml("version: 1\n")
    assert cfg.version == 1
    assert cfg.servers == []
    assert cfg.verl_case.cache_root == "/Users/Zhuanz/autoResearchData"
    assert cfg.verl_case.artifact_root == "/Users/Zhuanz/autoResearchData/runs"
    assert cfg.verl_case.model_id == "Qwen/Qwen3.5-2B"
    assert cfg.verl_case.dataset_id == "hiyouga/geometry3k"
    assert cfg.verl_case.ignore_eos is False
    assert cfg.verl_case.output_tokens == [2048, 4096, 8192, 16384]
    assert cfg.verl_case.dependency_repo_paths == {}
    assert cfg.verl_case.row_timeout_seconds == 7200
    assert cfg.verl_case.execution_profile == "fsdp"
    assert cfg.verl_case.rollout_gpu_memory_utilization == 0.5
    assert cfg.verl_case.rollout_max_model_len_floor == 24576
    assert cfg.verl_case.ppo_max_token_len_per_gpu_floor == 24576
    assert cfg.verl_case.rollout_update_weights_bucket_megabytes == 2048
    assert cfg.verl_case.use_remove_padding is None
    assert cfg.verl_case.use_dynamic_bsz is None


def test_from_yaml_with_servers():
    yaml_text = """
version: 1
servers:
  - name: nvidia-01
    host: 192.168.1.10
    port: 22
    user: t00906153
    identity_file: ~/.ssh/id_ed25519
"""
    cfg = from_yaml(yaml_text)
    assert len(cfg.servers) == 1
    s = cfg.servers[0]
    assert s.name == "nvidia-01"
    assert s.port == 22
    assert s.user == "t00906153"
    assert s.host == "192.168.1.10"
    assert s.workdir == "/root"


def test_from_yaml_verl_case_override():
    yaml_text = """
version: 1
verl_case:
  cache_root: /tmp/ar-cache
  artifact_root: /tmp/ar-data-runs
  output_tokens: [2048]
  inference_modes: [sync]
  row_timeout_seconds: 60
  execution_profile: fsdp2
  rollout_gpu_memory_utilization: 0.9
  rollout_max_model_len_floor: 0
  ppo_max_token_len_per_gpu_floor: 4096
  rollout_update_weights_bucket_megabytes: 512
  use_remove_padding: false
  use_dynamic_bsz: false
  dependency_repo_paths:
    verl: /home/t00906153/verl
"""
    cfg = from_yaml(yaml_text)
    assert cfg.verl_case.cache_root == "/tmp/ar-cache"
    assert cfg.verl_case.artifact_root == "/tmp/ar-data-runs"
    assert cfg.verl_case.output_tokens == [2048]
    assert cfg.verl_case.inference_modes == ["sync"]
    assert cfg.verl_case.row_timeout_seconds == 60
    assert cfg.verl_case.execution_profile == "fsdp2"
    assert cfg.verl_case.rollout_gpu_memory_utilization == 0.9
    assert cfg.verl_case.rollout_max_model_len_floor == 0
    assert cfg.verl_case.ppo_max_token_len_per_gpu_floor == 4096
    assert cfg.verl_case.rollout_update_weights_bucket_megabytes == 512
    assert cfg.verl_case.use_remove_padding is False
    assert cfg.verl_case.use_dynamic_bsz is False
    assert cfg.verl_case.dependency_repo_paths["verl"] == "/home/t00906153/verl"


def test_from_yaml_server_workdir_override():
    yaml_text = """
version: 1
servers:
  - name: nvidia-01
    host: 192.168.1.10
    user: t00906153
    workdir: /home/t00906153
"""
    cfg = from_yaml(yaml_text)
    assert cfg.servers[0].workdir == "/home/t00906153"


def test_from_yaml_resolves_env_placeholder(monkeypatch):
    monkeypatch.setenv("MY_TOKEN_XYZ", "secret_token_xyz")
    yaml_text = """
version: 1
servers:
  - name: srv
    host: h
    user: u
    bootstrap_password_secret: "<env:MY_TOKEN_XYZ>"
"""
    cfg = from_yaml(yaml_text)
    assert cfg.servers[0].bootstrap_password_secret == "secret_token_xyz"


def test_from_yaml_duplicate_server_names_raises():
    yaml_text = """
servers:
  - {name: a, host: h, user: u}
  - {name: a, host: h2, user: u2}
"""
    with pytest.raises(ConfigError) as exc:
        from_yaml(yaml_text)
    msg = str(exc.value)
    assert "name" in msg or "重复" in msg


def test_from_yaml_missing_required_field_chinese_error():
    yaml_text = """
servers:
  - host: h
    user: u
"""
    with pytest.raises(ConfigError) as exc:
        from_yaml(yaml_text)
    msg = str(exc.value)
    assert "配置错误" in msg
    assert "name" in msg  # 缺 name 字段


def test_from_yaml_invalid_port_chinese_error():
    yaml_text = """
servers:
  - {name: a, host: h, user: u, port: 99999}
"""
    with pytest.raises(ConfigError) as exc:
        from_yaml(yaml_text)
    assert "port" in str(exc.value)


def test_from_yaml_invalid_yaml_raises():
    with pytest.raises(ConfigError) as exc:
        from_yaml("invalid: yaml: with: bad: colons: but not really")
    assert "YAML" in str(exc.value) or "解析" in str(exc.value)


def test_from_yaml_non_dict_raises():
    with pytest.raises(ConfigError):
        from_yaml("- item1\n- item2\n")


def test_from_path_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "config.yaml").write_text("version: 1\nservers: []\n")
    cfg = from_path()
    assert cfg.version == 1


def test_from_path_env_override(tmp_path, monkeypatch):
    cfg_file = tmp_path / "my-config.yaml"
    cfg_file.write_text("version: 2\n")
    monkeypatch.setenv("AUTORESEARCH_CONFIG", str(cfg_file))
    cfg = from_path()
    assert cfg.version == 2


def test_from_path_missing_file_raises():
    with pytest.raises(ConfigError) as exc:
        from_path("/nonexistent/__path_does_not_exist_xyz__.yaml")
    assert "不存在" in str(exc.value)


def test_from_path_with_explicit_arg(tmp_path):
    cfg_file = tmp_path / "explicit.yaml"
    cfg_file.write_text("version: 3\nservers:\n  - name: x\n    host: h\n    user: u\n")
    cfg = from_path(cfg_file)
    assert cfg.version == 3
    assert cfg.servers[0].name == "x"
