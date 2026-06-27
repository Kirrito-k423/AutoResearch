---
name: rmb-cost-report
description: Generate RMB task cost reports from Codex/OpenAI-style token usage, including total input tokens, cached input tokens, uncached input tokens, output tokens, and GPT plus DeepSeek API cost estimates. Use when the user asks to统计 token 消耗, API 费用, 人民币成本, cache hit 成本, GPT/DeepSeek 对比, or to produce an `RMB-Cost.md` report for a task, goal, session, or experiment. Use by default for any goal, experiment, remote run, long command, or automation whose expected or actual runtime exceeds 20 minutes.
---

# RMB Cost Report

Use this skill to turn task token usage into a reproducible cost report named `RMB-Cost.md`.

## Workflow

1. Identify token usage:
   - Prefer structured usage from Codex session JSONL `token_count` events when available.
   - If the user already provides counts, use manual mode.
   - Treat `input_tokens` as total input, `cached_input_tokens` as cache hits, `input_tokens - cached_input_tokens` as cache misses, and `output_tokens` as billable output.
2. For any execution expected to exceed 20 minutes, start cost monitoring by preserving the goal/session start time and the likely session JSONL path; generate or update `RMB-Cost.md` when the execution finishes.
3. Verify current prices and USD/CNY when the user needs current or payable estimates. API and FX rates are time-sensitive.
4. Run `scripts/build_rmb_cost_report.py` to generate `RMB-Cost.md`.
5. Report the output path, the three component costs, and the total RMB costs for GPT and DeepSeek.

## Script

Use the bundled script without reimplementing the math:

```bash
python3 /Users/Zhuanz/.codex/skills/rmb-cost-report/scripts/build_rmb_cost_report.py \
  --session /path/to/rollout.jsonl \
  --start-ts 2026-06-25T04:32:14Z \
  --end-ts 2026-06-25T21:49:31Z \
  --goal-tokens-used 10729633 \
  --usd-cny 7.20 \
  --out RMB-Cost.md
```

Manual token mode:

```bash
python3 /Users/Zhuanz/.codex/skills/rmb-cost-report/scripts/build_rmb_cost_report.py \
  --input-tokens 320286130 \
  --cached-input-tokens 310518400 \
  --output-tokens 982791 \
  --goal-tokens-used 10729633 \
  --usd-cny 7.20 \
  --out RMB-Cost.md
```

Override prices when current official pricing differs:

```bash
python3 /Users/Zhuanz/.codex/skills/rmb-cost-report/scripts/build_rmb_cost_report.py \
  --input-tokens 1000000 --cached-input-tokens 700000 --output-tokens 50000 \
  --gpt-input-usd-per-mtok 5 --gpt-cached-usd-per-mtok 0.5 --gpt-output-usd-per-mtok 30 \
  --deepseek-input-usd-per-mtok 0.435 --deepseek-cached-usd-per-mtok 0.003625 --deepseek-output-usd-per-mtok 0.87 \
  --usd-cny 7.20 \
  --out RMB-Cost.md
```

## Reporting Rules

- Always include token quantities in raw tokens and M tokens.
- Always calculate and display the three billable components separately: uncached input, cached input, and output.
- Always include a model-level summary that adds the three components into total USD and total RMB.
- For executions that exceed 20 minutes, generate or update `RMB-Cost.md` by default even when the user did not explicitly ask for a cost report.
- Always state price assumptions, USD/CNY, and whether values were defaults or user-supplied.
- If Codex goal `tokensUsed` is known, include it as `Codex effective goal meter`; do not force it to equal raw session input/output totals.
- If prices or FX were not verified in the current turn, mark the report as an estimate.
