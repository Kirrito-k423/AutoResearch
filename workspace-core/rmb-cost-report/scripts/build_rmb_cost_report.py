#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOKEN_KEYS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


@dataclass(frozen=True)
class Price:
    name: str
    input_usd_per_mtok: float
    cached_usd_per_mtok: float
    output_usd_per_mtok: float
    note: str


DEFAULT_GPT = Price(
    name="gpt-5.5",
    input_usd_per_mtok=5.0,
    cached_usd_per_mtok=0.5,
    output_usd_per_mtok=30.0,
    note="Script default; verify current OpenAI pricing before payable use.",
)

DEFAULT_DEEPSEEK = Price(
    name="deepseek-v4-pro",
    input_usd_per_mtok=0.435,
    cached_usd_per_mtok=0.003625,
    output_usd_per_mtok=0.87,
    note="Script default; verify current DeepSeek pricing before payable use.",
)


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def empty_usage() -> dict[str, int]:
    return {key: 0 for key in TOKEN_KEYS}


def usage_from_event(obj: dict[str, Any]) -> dict[str, int] | None:
    payload = obj.get("payload") or {}
    if obj.get("type") != "event_msg" or payload.get("type") != "token_count":
        return None
    total = ((payload.get("info") or {}).get("total_token_usage") or {})
    return {key: int(total.get(key, 0) or 0) for key in TOKEN_KEYS}


def read_session_usage(path: Path, start_ts: datetime | None, end_ts: datetime | None) -> tuple[dict[str, int], dict[str, Any]]:
    before_start = empty_usage()
    end_usage: dict[str, int] | None = None
    first_usage: dict[str, int] | None = None
    first_ts: str | None = None
    end_seen_ts: str | None = None
    start_seen_ts: str | None = None
    event_count = 0

    with path.open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            usage = usage_from_event(obj)
            if usage is None:
                continue
            ts_text = obj.get("timestamp")
            ts = parse_ts(ts_text) if ts_text else None
            event_count += 1
            if first_usage is None:
                first_usage = usage
                first_ts = ts_text
            if start_ts and ts and ts < start_ts:
                before_start = usage
                start_seen_ts = ts_text
                continue
            if end_ts and ts and ts > end_ts:
                break
            end_usage = usage
            end_seen_ts = ts_text

    if end_usage is None:
        if first_usage is None:
            raise SystemExit(f"No token_count events found in {path}")
        end_usage = first_usage
        end_seen_ts = first_ts

    delta = {key: max(0, int(end_usage.get(key, 0)) - int(before_start.get(key, 0))) for key in TOKEN_KEYS}
    meta = {
        "session": str(path),
        "event_count_scanned": event_count,
        "base_event_ts": start_seen_ts,
        "end_event_ts": end_seen_ts,
    }
    return delta, meta


def cost_for(price: Price, input_tokens: int, cached_tokens: int, output_tokens: int, usd_cny: float) -> dict[str, float]:
    cached_tokens = min(cached_tokens, input_tokens)
    uncached_tokens = max(0, input_tokens - cached_tokens)
    uncached_usd = uncached_tokens / 1_000_000 * price.input_usd_per_mtok
    cached_usd = cached_tokens / 1_000_000 * price.cached_usd_per_mtok
    output_usd = output_tokens / 1_000_000 * price.output_usd_per_mtok
    total_usd = uncached_usd + cached_usd + output_usd
    return {
        "uncached_input_usd": uncached_usd,
        "cached_input_usd": cached_usd,
        "output_usd": output_usd,
        "total_usd": total_usd,
        "uncached_input_rmb": uncached_usd * usd_cny,
        "cached_input_rmb": cached_usd * usd_cny,
        "output_rmb": output_usd * usd_cny,
        "total_rmb": total_usd * usd_cny,
    }


def mtok(tokens: int) -> float:
    return tokens / 1_000_000


def money(value: float) -> str:
    if 0 < abs(value) < 0.01:
        return f"{value:,.6f}"
    if 0 < abs(value) < 1:
        return f"{value:,.4f}"
    return f"{value:,.2f}"


def number(value: int) -> str:
    return f"{value:,}"


def component_rows(price: Price, cost: dict[str, float], tokens: dict[str, int]) -> list[dict[str, str]]:
    return [
        {
            "component": "Input (cache miss)",
            "cache_status": "not cached",
            "tokens": number(tokens["uncached_input"]),
            "mtok": f"{mtok(tokens['uncached_input']):.6f}",
            "usd_per_mtok": f"{price.input_usd_per_mtok:g}",
            "usd": money(cost["uncached_input_usd"]),
            "rmb": money(cost["uncached_input_rmb"]),
        },
        {
            "component": "Input (cache hit)",
            "cache_status": "cached",
            "tokens": number(tokens["cached_input"]),
            "mtok": f"{mtok(tokens['cached_input']):.6f}",
            "usd_per_mtok": f"{price.cached_usd_per_mtok:g}",
            "usd": money(cost["cached_input_usd"]),
            "rmb": money(cost["cached_input_rmb"]),
        },
        {
            "component": "Output",
            "cache_status": "not applicable",
            "tokens": number(tokens["output"]),
            "mtok": f"{mtok(tokens['output']):.6f}",
            "usd_per_mtok": f"{price.output_usd_per_mtok:g}",
            "usd": money(cost["output_usd"]),
            "rmb": money(cost["output_rmb"]),
        },
    ]


def build_report(args: argparse.Namespace, usage: dict[str, int], meta: dict[str, Any]) -> str:
    input_tokens = int(usage["input_tokens"])
    cached_tokens = min(int(usage["cached_input_tokens"]), input_tokens)
    uncached_tokens = max(0, input_tokens - cached_tokens)
    output_tokens = int(usage["output_tokens"])
    reasoning_tokens = int(usage.get("reasoning_output_tokens", 0))

    gpt = Price(
        name=args.gpt_name,
        input_usd_per_mtok=args.gpt_input_usd_per_mtok,
        cached_usd_per_mtok=args.gpt_cached_usd_per_mtok,
        output_usd_per_mtok=args.gpt_output_usd_per_mtok,
        note=args.gpt_note,
    )
    deepseek = Price(
        name=args.deepseek_name,
        input_usd_per_mtok=args.deepseek_input_usd_per_mtok,
        cached_usd_per_mtok=args.deepseek_cached_usd_per_mtok,
        output_usd_per_mtok=args.deepseek_output_usd_per_mtok,
        note=args.deepseek_note,
    )
    rows = [
        (gpt, cost_for(gpt, input_tokens, cached_tokens, output_tokens, args.usd_cny)),
        (deepseek, cost_for(deepseek, input_tokens, cached_tokens, output_tokens, args.usd_cny)),
    ]
    billable_tokens = {
        "uncached_input": uncached_tokens,
        "cached_input": cached_tokens,
        "output": output_tokens,
    }
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    confidence = "verified" if args.verified else "estimate"

    lines = [
        "# RMB Cost",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Confidence: `{confidence}`",
        f"- USD/CNY: `{args.usd_cny}`",
    ]
    if args.task_name:
        lines.append(f"- Task: {args.task_name}")
    if args.goal_tokens_used is not None:
        lines.append(f"- Codex effective goal meter: `{number(args.goal_tokens_used)}` tokens ({mtok(args.goal_tokens_used):.6f}M)")
    if meta:
        if meta.get("session"):
            lines.append(f"- Session: `{meta['session']}`")
        if meta.get("base_event_ts") or meta.get("end_event_ts"):
            lines.append(f"- Token window events: `{meta.get('base_event_ts')}` -> `{meta.get('end_event_ts')}`")
    lines.extend(
        [
            "",
            "## Token Usage",
            "",
            "| Item | Tokens | M tokens |",
            "|---|---:|---:|",
            f"| Input total | {number(input_tokens)} | {mtok(input_tokens):.6f} |",
            f"| Cached input | {number(cached_tokens)} | {mtok(cached_tokens):.6f} |",
            f"| Uncached input | {number(uncached_tokens)} | {mtok(uncached_tokens):.6f} |",
            f"| Output | {number(output_tokens)} | {mtok(output_tokens):.6f} |",
            f"| Reasoning output, included in output when provider reports it that way | {number(reasoning_tokens)} | {mtok(reasoning_tokens):.6f} |",
            "",
            "## Price Assumptions",
            "",
            "| Model | Input USD/M | Cached input USD/M | Output USD/M | Note |",
            "|---|---:|---:|---:|---|",
            f"| {gpt.name} | {gpt.input_usd_per_mtok:g} | {gpt.cached_usd_per_mtok:g} | {gpt.output_usd_per_mtok:g} | {gpt.note} |",
            f"| {deepseek.name} | {deepseek.input_usd_per_mtok:g} | {deepseek.cached_usd_per_mtok:g} | {deepseek.output_usd_per_mtok:g} | {deepseek.note} |",
            "",
            "## Cost Breakdown",
            "",
            "| Model | Component | Cache status | Tokens | M tokens | USD/M | USD | RMB |",
            "|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for price, cost in rows:
        for component in component_rows(price, cost, billable_tokens):
            lines.append(
                f"| {price.name} | {component['component']} | {component['cache_status']} | "
                f"{component['tokens']} | {component['mtok']} | {component['usd_per_mtok']} | "
                f"{component['usd']} | {component['rmb']} |"
            )
    lines.extend(
        [
            "",
            "## Cost Summary",
            "",
            "| Model | Input cache miss RMB | Input cache hit RMB | Output RMB | Total RMB | Total USD |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for price, cost in rows:
        lines.append(
            f"| {price.name} | {money(cost['uncached_input_rmb'])} | {money(cost['cached_input_rmb'])} | "
            f"{money(cost['output_rmb'])} | {money(cost['total_rmb'])} | {money(cost['total_usd'])} |"
        )
    lines.extend(
        [
            "",
            "## Formula",
            "",
            "`uncached_input = input_total - cached_input`",
            "",
            "`uncached_input_cost = uncached_input_M * input_usd_per_M`",
            "",
            "`cached_input_cost = cached_input_M * cached_input_usd_per_M`",
            "",
            "`output_cost = output_M * output_usd_per_M`",
            "",
            "`total_rmb = (uncached_input_cost + cached_input_cost + output_cost) * USD_CNY`",
            "",
            "## Notes",
            "",
            "- Re-run with current official API prices and FX before using this for reimbursement or budget approval.",
            "- Codex goal `tokensUsed` can differ from raw session input/output because it is an effective meter, while session logs also expose cache hits and repeated context reads.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate RMB-Cost.md from token usage.")
    source = parser.add_argument_group("usage source")
    source.add_argument("--session", type=Path, help="Codex session JSONL with token_count events.")
    source.add_argument("--start-ts", help="UTC or ISO timestamp for the usage window start.")
    source.add_argument("--end-ts", help="UTC or ISO timestamp for the usage window end.")
    source.add_argument("--input-tokens", type=int, help="Manual total input tokens.")
    source.add_argument("--cached-input-tokens", type=int, default=0, help="Manual cached input tokens.")
    source.add_argument("--output-tokens", type=int, help="Manual output tokens.")
    source.add_argument("--reasoning-output-tokens", type=int, default=0, help="Manual reasoning output tokens.")
    source.add_argument("--goal-tokens-used", type=int, help="Optional Codex goal effective token meter.")
    source.add_argument("--task-name", help="Optional task name for the report.")

    pricing = parser.add_argument_group("pricing")
    pricing.add_argument("--usd-cny", type=float, default=7.20, help="USD to CNY exchange rate. Default is a placeholder estimate.")
    pricing.add_argument("--verified", action="store_true", help="Mark price and FX assumptions as verified for this run.")
    pricing.add_argument("--gpt-name", default=DEFAULT_GPT.name)
    pricing.add_argument("--gpt-input-usd-per-mtok", type=float, default=DEFAULT_GPT.input_usd_per_mtok)
    pricing.add_argument("--gpt-cached-usd-per-mtok", type=float, default=DEFAULT_GPT.cached_usd_per_mtok)
    pricing.add_argument("--gpt-output-usd-per-mtok", type=float, default=DEFAULT_GPT.output_usd_per_mtok)
    pricing.add_argument("--gpt-note", default=DEFAULT_GPT.note)
    pricing.add_argument("--deepseek-name", default=DEFAULT_DEEPSEEK.name)
    pricing.add_argument("--deepseek-input-usd-per-mtok", type=float, default=DEFAULT_DEEPSEEK.input_usd_per_mtok)
    pricing.add_argument("--deepseek-cached-usd-per-mtok", type=float, default=DEFAULT_DEEPSEEK.cached_usd_per_mtok)
    pricing.add_argument("--deepseek-output-usd-per-mtok", type=float, default=DEFAULT_DEEPSEEK.output_usd_per_mtok)
    pricing.add_argument("--deepseek-note", default=DEFAULT_DEEPSEEK.note)

    parser.add_argument("--out", type=Path, default=Path("RMB-Cost.md"), help="Output markdown path.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    meta: dict[str, Any] = {}

    if args.session:
        usage, meta = read_session_usage(args.session, parse_ts(args.start_ts), parse_ts(args.end_ts))
    else:
        if args.input_tokens is None or args.output_tokens is None:
            parser.error("Provide either --session or both --input-tokens and --output-tokens.")
        usage = {
            "input_tokens": args.input_tokens,
            "cached_input_tokens": args.cached_input_tokens,
            "output_tokens": args.output_tokens,
            "reasoning_output_tokens": args.reasoning_output_tokens,
            "total_tokens": args.input_tokens + args.output_tokens,
        }

    report = build_report(args, usage, meta)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(json.dumps({"out": str(args.out), "input_tokens": usage["input_tokens"], "cached_input_tokens": usage["cached_input_tokens"], "output_tokens": usage["output_tokens"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
