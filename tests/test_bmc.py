"""autoresearch.bmc — Redfish 客户端 + identify + power 单测 (全 mock, 不动真机)."""
from __future__ import annotations

from unittest.mock import MagicMock, patch
import base64
import json

import pytest

from autoresearch.bmc.client import (
    BMCClient,
    BMCError,
    BMCPowerState,
    build_bmc_client,
)
from autoresearch.bmc.identify import identify_server
from autoresearch.bmc.power import power_status, power_off, power_on, power_cycle
from workspace_core.config import BMCSpec


def _bmc_spec(**overrides) -> BMCSpec:
    base = dict(
        host="192.168.12.182",
        port=443,
        user="Administrator",
        password="Admin@9000",
        protocol="redfish",
        power_operations_allowed=False,
    )
    base.update(overrides)
    return BMCSpec(**base)


def _mock_response(json_body: dict | None = None, status_code: int = 200, text: str = "") -> MagicMock:
    r = MagicMock()
    r.status_code = status_code
    r.json.return_value = json_body if json_body is not None else {}
    r.text = text or (json.dumps(json_body) if json_body is not None else "")
    return r


# === client.py ===


def test_bmc_client_basic_auth_header_built_from_user_password():
    spec = _bmc_spec(user="Administrator", password="Admin@9000")
    client = BMCClient(spec)
    expected = base64.b64encode(b"Administrator:Admin@9000").decode("ascii")
    assert client._session.headers["Authorization"] == f"Basic {expected}"
    assert client.base_url == "https://192.168.12.182:443"
    client.close()


def test_bmc_client_get_returns_dict_and_raises_on_non_200():
    spec = _bmc_spec()
    client = BMCClient(spec)
    with patch.object(client._session, "get") as gget:
        gget.return_value = _mock_response({"ok": True})
        result = client.get_service_root()
        assert result == {"ok": True}
    with patch.object(client._session, "get") as gget:
        gget.return_value = _mock_response(text="denied", status_code=401)
        with pytest.raises(BMCError) as exc:
            client.get_service_root()
        assert "HTTP 401" in str(exc.value)
    client.close()


def test_bmc_client_post_passes_resettype_body():
    spec = _bmc_spec()
    client = BMCClient(spec)
    with patch.object(client._session, "post") as gpost:
        gpost.return_value = _mock_response(text="ok", status_code=200)
        status, body = client.reset_system("ForceOff")
        assert status == 200
        sent = gpost.call_args.kwargs["json"]
        assert sent == {"ResetType": "ForceOff"}
    client.close()


# === identify.py ===


def test_identify_server_returns_bmc_identifier_with_priority_uuid_serial_sku():
    spec = _bmc_spec()
    # Patch build_bmc_client 返回 mock client
    fake_client = MagicMock()
    fake_client.get_managers.return_value = ["/redfish/v1/Managers/1"]
    fake_client.get_manager_info.return_value = {
        "UUID": "11111111-2222-3333-4444-555555555555",
        "HostName": "ax182-bmc",
    }
    fake_client.get_systems.return_value = ["/redfish/v1/Systems/1"]
    fake_client.get_system_info.return_value = {
        "SerialNumber": "2102311BQH10E5000123",
        "SKU": "Atlas 800T A2",
        "Model": "Atlas 800T A2",
        "Manufacturer": "Huawei",
        "PowerState": "On",
    }
    with patch("autoresearch.bmc.identify.build_bmc_client", return_value=fake_client):
        result = identify_server(spec)
    assert result["ok"] is True
    data = result["data"]
    assert data["bmc_uuid"] == "11111111-2222-3333-4444-555555555555"
    assert data["system_serial"] == "2102311BQH10E5000123"
    assert data["bmc_identifier"] == "11111111-2222-3333-4444-555555555555"  # UUID 优先
    assert data["power_state"] == "On"


def test_identify_server_falls_back_to_serial_when_uuid_missing():
    spec = _bmc_spec()
    fake_client = MagicMock()
    fake_client.get_managers.return_value = ["/redfish/v1/Managers/1"]
    fake_client.get_manager_info.return_value = {"UUID": None, "HostName": "x"}
    fake_client.get_systems.return_value = ["/redfish/v1/Systems/1"]
    fake_client.get_system_info.return_value = {
        "SerialNumber": "SER-001",
        "SKU": "SKU-001",
        "Model": "M",
        "Manufacturer": "H",
        "PowerState": "Off",
    }
    with patch("autoresearch.bmc.identify.build_bmc_client", return_value=fake_client):
        result = identify_server(spec)
    assert result["ok"] is True
    assert result["data"]["bmc_identifier"] == "SER-001"


def test_identify_server_fail_when_all_identifiers_empty():
    spec = _bmc_spec()
    fake_client = MagicMock()
    fake_client.get_managers.return_value = ["/redfish/v1/Managers/1"]
    fake_client.get_manager_info.return_value = {"UUID": None, "HostName": None}
    fake_client.get_systems.return_value = ["/redfish/v1/Systems/1"]
    fake_client.get_system_info.return_value = {
        "SerialNumber": None, "SKU": None, "Model": None,
        "Manufacturer": None, "PowerState": None,
    }
    with patch("autoresearch.bmc.identify.build_bmc_client", return_value=fake_client):
        result = identify_server(spec)
    assert result["ok"] is False
    assert "BMC 未返回任何唯一编码" in result["message"]


# === power.py: 默认 dry-run + power_operations_allowed 拒绝 ===


def test_power_off_dry_run_when_apply_false():
    spec = _bmc_spec(power_operations_allowed=True)  # 授权了但不加 --apply
    result = power_off(spec, apply=False)
    assert result["ok"] is True
    assert result["data"]["would_send"] == "ForceOff"
    assert "DRY-RUN" in result["message"]


def test_power_off_refused_when_power_operations_allowed_false():
    spec = _bmc_spec(power_operations_allowed=False)  # 默认
    result = power_off(spec, apply=True)  # 即使显式 --apply
    assert result["ok"] is False
    assert "power_operations_allowed=false" in result["error"]
    assert "refuse" in result["message"]


def test_power_on_apply_posts_resettype_on():
    spec = _bmc_spec(power_operations_allowed=True)
    fake_client = MagicMock()
    fake_client.reset_system.return_value = (200, "ok")
    with patch("autoresearch.bmc.power.build_bmc_client", return_value=fake_client):
        result = power_on(spec, apply=True)
    assert result["ok"] is True
    assert fake_client.reset_system.called
    assert fake_client.reset_system.call_args.args[0] == "On"


def test_power_cycle_apply_posts_powercycle():
    spec = _bmc_spec(power_operations_allowed=True)
    fake_client = MagicMock()
    fake_client.reset_system.return_value = (202, "accepted")
    with patch("autoresearch.bmc.power.build_bmc_client", return_value=fake_client):
        result = power_cycle(spec, apply=True)
    assert result["ok"] is True
    assert fake_client.reset_system.call_args.args[0] == "PowerCycle"


def test_power_status_returns_powerstate():
    spec = _bmc_spec()
    fake_client = MagicMock()
    fake_client.get_power_state.return_value = BMCPowerState.ON
    with patch("autoresearch.bmc.power.build_bmc_client", return_value=fake_client):
        result = power_status(spec)
    assert result["ok"] is True
    assert result["data"]["power_state"] == "On"
    # 状态查询不需要 power_operations_allowed, 也不需要 apply 参数
    assert "BMC 电源状态" in result["message"]


def test_power_off_network_error_returns_fail():
    spec = _bmc_spec(power_operations_allowed=True)
    fake_client = MagicMock()
    fake_client.reset_system.side_effect = BMCError("network down")
    with patch("autoresearch.bmc.power.build_bmc_client", return_value=fake_client):
        result = power_off(spec, apply=True)
    assert result["ok"] is False
    assert "network down" in result["error"]
