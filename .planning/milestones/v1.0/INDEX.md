# AutoResearch v1.0 MinViable Loop Archive

**Status:** shipped on 2026-06-15
**Phases:** 1-13
**Plans:** 37 summaries after Phase 13
**Requirements:** 82/88 checked; 6 known gaps archived as follow-up context

## Snapshot Files

- `ROADMAP.md` — final v1.0 roadmap snapshot before living roadmap collapse
- `REQUIREMENTS.md` — archived v1.0 requirements, including known gaps
- `PROJECT.md` — project intent and constraints snapshot
- `STATE.md` — state snapshot after Phase 12 ship and before Phase 13 close

## Validation Evidence

- `uv run pytest -q` -> 361 passed, 6 warnings
- `uv run autoresearch check all --server A2-AK-225 --stack-lib verl` -> ok
- `uv run autoresearch run smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` -> ok
- `uv run autoresearch e2e smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` -> ok
- E2E run id: `01KV62JVH0N3ZRVRMH4PYWF1VB`
- E2E report: `/Users/Zhuanz/.autoresearch/runs/01KV62JVH0N3ZRVRMH4PYWF1VB/report.html`

## Known Gaps

- HW-CONN-01 / HW-CONN-02 remain partially constrained by multi-server SSH/BMC reality.
- HW-OCC-01 / HW-OCC-02 remain constrained by current `npu-smi` process table availability in real UAT.
- NET-TUNNEL-01 / NET-TUNNEL-02 implementation exists and A2-AK-225 passed, but all-server UAT remains incomplete.
- Open artifact audit reported Phase 04 UAT as `partial` and Phase 12 UAT as `passed` with zero pending scenarios.
