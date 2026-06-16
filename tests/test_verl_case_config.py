"""Tests for Phase 14 Verl formal-case config and evaluation helpers."""
from __future__ import annotations

import importlib
from datetime import datetime, timezone


case_config = importlib.import_module("workspace-adapter.verl.case_config")
evaluation = importlib.import_module("workspace-adapter.verl.evaluation")


def test_default_matrix_has_sync_async_lengths():
    config = case_config.VerlCaseConfig()

    rows = case_config.build_length_matrix(config)

    assert len(rows) == 8
    assert {(r.output_tokens, r.inference_mode) for r in rows} == {
        (2048, "sync"),
        (2048, "async"),
        (4096, "sync"),
        (4096, "async"),
        (8192, "sync"),
        (8192, "async"),
        (16384, "sync"),
        (16384, "async"),
    }
    assert all(r.input_tokens == 1024 for r in rows)
    assert all(r.ignore_eos is False for r in rows)


def test_immutable_config_snapshot_has_second_timestamp(tmp_path):
    created_at = datetime(2026, 6, 16, 8, 9, 10, tzinfo=timezone.utc)
    config = case_config.VerlCaseConfig()
    run_config = case_config.VerlCaseRunConfig(
        run_id="run123",
        created_at=created_at,
        server="A2-AK-225",
        config=config,
        matrix=case_config.build_length_matrix(config),
        provenance=[
            case_config.RepoProvenance(repo="AutoResearch", commit_sha="abc123")
        ],
    )

    path = case_config.write_immutable_config(run_config, tmp_path)

    assert path.name == "config-20260616T080910.json"
    text = path.read_text(encoding="utf-8")
    assert '"run_id": "run123"' in text
    assert '"ignore_eos": false' in text
    assert "secret" not in text.lower()


def test_accuracy_answer_extraction_and_consistency():
    assert evaluation.extract_final_answer(r"The answer is \\boxed{42}.") == "42"
    assert evaluation.score_ground_truth("Answer: 42", "42") is True
    assert evaluation.score_sync_async_consistency(" The answer is A ", "a") is True
    assert evaluation.score_ground_truth("Answer: 41", "42") is False
