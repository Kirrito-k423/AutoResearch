"""Tests for Verl stage timing extraction."""
from __future__ import annotations

import importlib
import json


stage_timing = importlib.import_module("workspace-adapter.verl.stage_timing")


def test_normalize_stage_metric_key_maps_known_grpo_phases():
    assert stage_timing.normalize_stage_metric_key("timing/rollout_generate_seconds") == "rollout"
    assert stage_timing.normalize_stage_metric_key("actor/ref_log_prob_time") == "ref_logp"
    assert stage_timing.normalize_stage_metric_key("actor/log_prob_time") == "logp"
    assert stage_timing.normalize_stage_metric_key("reward_model/reward_time") == "reward"
    assert stage_timing.normalize_stage_metric_key("advantage/compute_time") == "advantage"
    assert stage_timing.normalize_stage_metric_key("actor/optimizer_step_time") == "update"
    assert stage_timing.normalize_stage_metric_key("val-core/validation_time") == "validation"
    assert stage_timing.normalize_stage_metric_key("trainer/save_checkpoint_time") == "checkpointing"
    assert stage_timing.normalize_stage_metric_key("data/dataloader_time") == "data_loading"


def test_extract_stage_timings_from_wandb_history_jsonl(tmp_path):
    run_dir = tmp_path / "wandb" / "source-runs" / "offline-run-1" / "files"
    run_dir.mkdir(parents=True)
    (run_dir / "wandb-history.jsonl").write_text(
        json.dumps(
            {
                "_step": 1,
                "timing/rollout_generate_seconds": 1.25,
                "actor/ref_log_prob_time": 0.5,
                "actor/log_prob_time_ms": 250,
                "perf/tokens_per_second": 123,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    rows = stage_timing.extract_stage_timings_from_wandb_run(
        tmp_path / "wandb",
        run_id="run123",
        case_id="case-a",
    )

    assert {row.stage for row in rows} == {"rollout", "ref_logp", "logp"}
    assert {row.source for row in rows} == {"wandb"}
    assert all(row.step == 1 for row in rows)
    logp = next(row for row in rows if row.stage == "logp")
    assert logp.elapsed_seconds == 0.25
    assert logp.original_key == "actor/log_prob_time_ms"


def test_extract_stage_timings_preserves_unknown_timing_keys(tmp_path):
    files = tmp_path / "files"
    files.mkdir()
    (files / "wandb-summary.json").write_text(
        json.dumps({"_step": 3, "timing/custom_phase_seconds": 2.0}),
        encoding="utf-8",
    )

    rows = stage_timing.extract_stage_timings_from_wandb_run(
        tmp_path,
        run_id="run123",
        case_id="case-a",
    )

    assert len(rows) == 1
    assert rows[0].stage == "other"
    assert rows[0].original_key == "timing/custom_phase_seconds"
    assert rows[0].elapsed_seconds == 2.0


def test_extract_stage_timings_missing_wandb_dir_returns_empty(tmp_path):
    assert stage_timing.extract_stage_timings_from_wandb_run(
        tmp_path / "missing",
        run_id="run123",
        case_id="case-a",
    ) == []
