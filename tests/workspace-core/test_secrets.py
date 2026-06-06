"""Tests for secrets resolver (D-06..09)."""
import pytest

from workspace_core.secrets import resolver
from workspace_core.secrets import resolve_secret, SecretError


def test_resolve_secret_passthrough():
    """非占位符原样返回."""
    assert resolve_secret("plain text") == "plain text"
    assert resolve_secret("") == ""
    assert resolve_secret("not-a-placeholder") == "not-a-placeholder"


def test_resolve_env_placeholder(monkeypatch):
    monkeypatch.setenv("TEST_SECRET_XYZ", "env_value_456")
    assert resolve_secret("<env:TEST_SECRET_XYZ>") == "env_value_456"


def test_resolve_env_placeholder_missing_raises(monkeypatch):
    monkeypatch.delenv("NONEXISTENT_VAR_XYZ", raising=False)
    with pytest.raises(SecretError) as exc:
        resolve_secret("<env:NONEXISTENT_VAR_XYZ>")
    assert "NONEXISTENT_VAR_XYZ" in str(exc.value)


def test_resolve_keyring_falls_back_to_env(monkeypatch):
    """D-09 软失败: keyring 不可用时 fallback env."""
    import keyring
    monkeypatch.setattr(keyring, "get_password", lambda *a, **kw: None)
    monkeypatch.setenv("MY_SECRET_FALLBACK", "fallback_value")
    assert resolve_secret("<keyring:MY_SECRET_FALLBACK>") == "fallback_value"


def test_resolve_keyring_uses_real_keyring(monkeypatch):
    """当 keyring 能返回非 None 时, 用 keyring 值."""
    import keyring
    monkeypatch.setattr(keyring, "get_password", lambda service, name: f"keyring-{name}")
    assert resolve_secret("<keyring:MY_KEY>") == "keyring-MY_KEY"


def test_resolve_keyring_no_value_no_env_raises(monkeypatch):
    """keyring 返 None + env 不存在 → SecretError."""
    import keyring
    monkeypatch.setattr(keyring, "get_password", lambda *a, **kw: None)
    monkeypatch.delenv("MISSING_VAR", raising=False)
    with pytest.raises(SecretError):
        resolve_secret("<keyring:MISSING_VAR>")


def test_resolve_dict_recursive():
    """dict 中嵌套 dict / list 的占位符都解."""
    from workspace_core.secrets import resolve_dict
    out = resolve_dict({
        "a": "<env:HOME>",
        "b": {"c": "<env:USER>", "d": "plain"},
        "e": ["<env:PATH>", "literal", {"f": "<env:LANG>"}],
    })
    import os
    assert out["a"] == os.environ.get("HOME")
    assert out["b"]["c"] == os.environ.get("USER")
    assert out["b"]["d"] == "plain"
    assert out["e"][0] == os.environ.get("PATH")
    assert out["e"][1] == "literal"
    assert out["e"][2]["f"] == os.environ.get("LANG")


def test_secret_error_message_includes_placeholder():
    """错误信息含占位符字符串."""
    with pytest.raises(SecretError) as exc:
        resolve_secret("<env:__TEST_MISSING_SECRET__>")
    assert "<env:__TEST_MISSING_SECRET__>" in str(exc.value)
