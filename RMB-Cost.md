# RMB Cost

- Generated at: `2026-06-26T04:40:35Z`
- Confidence: `estimate`
- USD/CNY: `7.2`
- Task: Qwen3.5 35B GRPO AutoResearch
- Codex effective goal meter: `10,729,633` tokens (10.729633M)
- Session: `/Users/Zhuanz/.codex/sessions/2026/06/25/rollout-2026-06-25T12-31-17-019efd0b-eca7-79c1-a7d3-dca562ba19d4.jsonl`
- Token window events: `2026-06-25T04:32:01.978Z` -> `2026-06-25T21:49:31.904Z`

## Token Usage

| Item | Tokens | M tokens |
|---|---:|---:|
| Input total | 320,286,130 | 320.286130 |
| Cached input | 310,518,400 | 310.518400 |
| Uncached input | 9,767,730 | 9.767730 |
| Output | 982,791 | 0.982791 |
| Reasoning output, included in output when provider reports it that way | 206,956 | 0.206956 |

## Price Assumptions

| Model | Input USD/M | Cached input USD/M | Output USD/M | Note |
|---|---:|---:|---:|---|
| gpt-5.5 | 5 | 0.5 | 30 | Script default; verify current OpenAI pricing before payable use. |
| deepseek-v4-pro | 0.435 | 0.003625 | 0.87 | Script default; verify current DeepSeek pricing before payable use. |

## Cost Breakdown

| Model | Component | Cache status | Tokens | M tokens | USD/M | USD | RMB |
|---|---|---|---:|---:|---:|---:|---:|
| gpt-5.5 | Input (cache miss) | not cached | 9,767,730 | 9.767730 | 5 | 48.84 | 351.64 |
| gpt-5.5 | Input (cache hit) | cached | 310,518,400 | 310.518400 | 0.5 | 155.26 | 1,117.87 |
| gpt-5.5 | Output | not applicable | 982,791 | 0.982791 | 30 | 29.48 | 212.28 |
| deepseek-v4-pro | Input (cache miss) | not cached | 9,767,730 | 9.767730 | 0.435 | 4.25 | 30.59 |
| deepseek-v4-pro | Input (cache hit) | cached | 310,518,400 | 310.518400 | 0.003625 | 1.13 | 8.10 |
| deepseek-v4-pro | Output | not applicable | 982,791 | 0.982791 | 0.87 | 0.8550 | 6.16 |

## Cost Summary

| Model | Input cache miss RMB | Input cache hit RMB | Output RMB | Total RMB | Total USD |
|---|---:|---:|---:|---:|---:|
| gpt-5.5 | 351.64 | 1,117.87 | 212.28 | 1,681.79 | 233.58 |
| deepseek-v4-pro | 30.59 | 8.10 | 6.16 | 44.85 | 6.23 |

## Formula

`uncached_input = input_total - cached_input`

`uncached_input_cost = uncached_input_M * input_usd_per_M`

`cached_input_cost = cached_input_M * cached_input_usd_per_M`

`output_cost = output_M * output_usd_per_M`

`total_rmb = (uncached_input_cost + cached_input_cost + output_cost) * USD_CNY`

## Notes

- Re-run with current official API prices and FX before using this for reimbursement or budget approval.
- Codex goal `tokensUsed` can differ from raw session input/output because it is an effective meter, while session logs also expose cache hits and repeated context reads.
