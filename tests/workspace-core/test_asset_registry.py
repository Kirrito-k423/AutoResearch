from __future__ import annotations

from pathlib import Path

import yaml

from workspace_core.asset_registry import (
    load_registry,
    local_path_for_asset,
    select_remote_location,
    update_asset_record,
)


def test_load_registry_falls_back_to_sibling_example(tmp_path: Path):
    example = tmp_path / "data.example.yaml"
    example.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "assets": {
                    "models": {
                        "qwen": {
                            "canonical_id": "Qwen/Qwen3.5-2B",
                            "local": {"path": str(tmp_path / "model")},
                        }
                    }
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    registry = load_registry(tmp_path / "data.yaml")
    path = local_path_for_asset(
        kind="model",
        canonical_id="Qwen/Qwen3.5-2B",
        cache_root=tmp_path / "fallback",
        data_config_path=tmp_path / "data.yaml",
    )

    assert registry["version"] == 1
    assert path == tmp_path / "model"


def test_update_asset_record_starts_from_sibling_example(tmp_path: Path):
    example = tmp_path / "data.example.yaml"
    example.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "assets": {
                    "datasets": {
                        "geo3k": {
                            "kind": "dataset",
                            "canonical_id": "hiyouga/geometry3k",
                            "sources": {
                                "huggingface": {
                                    "id": "hiyouga/geometry3k",
                                    "url": "https://huggingface.co/datasets/hiyouga/geometry3k",
                                }
                            },
                        }
                    }
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    update_asset_record(
        kind="dataset",
        canonical_id="hiyouga/geometry3k",
        data_config_path=tmp_path / "data.yaml",
        status="ready",
        local_path=tmp_path / "datasets" / "geo3k",
    )
    registry = yaml.safe_load((tmp_path / "data.yaml").read_text(encoding="utf-8"))

    entry = registry["assets"]["datasets"]["geo3k"]
    assert entry["sources"]["huggingface"]["id"] == "hiyouga/geometry3k"
    assert entry["status"] == "ready"
    assert entry["local"]["path"] == str(tmp_path / "datasets" / "geo3k")


def test_update_asset_record_accumulates_remote_locations(tmp_path: Path):
    data_config = tmp_path / "data.yaml"

    update_asset_record(
        kind="model",
        canonical_id="Qwen/Qwen3.5-35B-A3B",
        data_config_path=data_config,
        status="ready",
        remote_server="A2-AK-225",
        remote_host="192.168.9.225",
        remote_path="/home/t00906153/autoresearch-assets/models/Qwen__Qwen3.5-35B-A3B",
    )
    update_asset_record(
        kind="model",
        canonical_id="Qwen/Qwen3.5-35B-A3B",
        data_config_path=data_config,
        status="ready",
        remote_server="A3-AX-180",
        remote_host="192.168.13.180",
        remote_path="/home/t00906153/autoresearch-assets/models/Qwen__Qwen3.5-35B-A3B",
    )
    registry = yaml.safe_load(data_config.read_text(encoding="utf-8"))
    entry = registry["assets"]["models"]["qwen3-5-35b-a3b"]

    assert set(entry["remotes"]) == {"A2-AK-225", "A3-AX-180"}
    selected = select_remote_location(
        entry,
        server_name="A2-AK-225",
        host="192.168.9.225",
    )
    assert selected == {
        "server": "A2-AK-225",
        "host": "192.168.9.225",
        "path": "/home/t00906153/autoresearch-assets/models/Qwen__Qwen3.5-35B-A3B",
    }
