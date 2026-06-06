"""Tests for config loader (D-10..13)."""
import os
import pytest

from workspace_core.config import from_yaml, from_path, ConfigError


def test_from_yaml_minimal():
    cfg = from_yaml("version: 1\n")
    assert cfg.version == 1
    assert cfg.servers == []


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
