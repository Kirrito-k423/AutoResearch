"""Tests for Phase 14 Verl formal-case config and evaluation helpers."""
from __future__ import annotations

import importlib
import re
from datetime import datetime, timedelta, timezone


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


def test_training_tuning_defaults_start_single_card_bs1():
    config = case_config.VerlCaseConfig()

    rows = case_config.build_training_tuning_matrix(config)

    assert config.case_mode == "training"
    assert config.trainer_val_only is False
    assert config.training_steps == 3
    assert config.execution_profile == "fsdp"
    assert config.use_remove_padding is None
    assert config.use_dynamic_bsz is None
    assert config.single_card_start_batch_size == 1
    assert config.single_card_devices == [0]
    assert config.single_node_devices == list(range(8))
    assert rows[0].device_count == 1
    assert rows[0].visible_devices == [0]
    assert rows[0].train_batch_size == 1
    assert rows[0].input_tokens == 1024
    assert rows[0].output_tokens == 2048
    assert rows[0].case_id.startswith("train-1npu-bs1-")


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


def test_readable_run_id_names_model_algorithm_lengths_and_time():
    created_at = datetime(2026, 6, 22, 14, 50, 1, tzinfo=timezone.utc)
    config = case_config.VerlCaseConfig(
        input_tokens=1024,
        output_tokens=[2048, 16384],
        inference_modes=["sync", "async"],
        trainer_val_only=True,
        ignore_eos=False,
    )

    run_id = case_config.build_readable_run_id(config, created_at)

    assert run_id.startswith("Qwen35-2B-GRPO-1Kto16K-")
    assert re.search(r"-\d{6}d-\d{6}s-", run_id)
    assert run_id.endswith("-valonly-modes-sync-async-noignoreeos")


def test_wandb_run_name_names_single_matrix_row():
    created_at = datetime(2026, 6, 22, 14, 50, 1, tzinfo=timezone(timedelta(hours=8)))
    config = case_config.VerlCaseConfig(
        input_tokens=1024,
        output_tokens=[4096],
        inference_modes=["async"],
        trainer_val_only=True,
        ignore_eos=False,
    )
    row = case_config.VerlCaseMatrixRow(
        input_tokens=1024,
        output_tokens=4096,
        inference_mode="async",
        ignore_eos=False,
    )

    run_name = case_config.build_wandb_run_name(config, row, created_at)

    assert run_name == "Qwen35-2B-GRPO-1Kto4K-260622d-145001s-valonly-async-noignoreeos"


def test_accuracy_answer_extraction_and_consistency():
    assert evaluation.extract_final_answer(r"The answer is \\boxed{42}.") == "42"
    assert evaluation.score_ground_truth("Answer: 42", "42") is True
    assert evaluation.score_sync_async_consistency(" The answer is A ", "a") is True
    assert evaluation.score_ground_truth("Answer: 41", "42") is False
