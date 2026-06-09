# Phase 5: Skill 04 — network-check - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-09
**Phase:** 5-Skill 04 — network-check
**Areas discussed:** CLI and output, network matrix semantics, proxy fallback, tunnel lifecycle, UAT gate

---

## Batch 1 — CLI, JSON, Severity, Curl, Proxy Trigger

| Question | Selected |
|----------|----------|
| CLI default | `net probe` defaults to local + all remote servers |
| JSON shape | Primary flat `rows` plus grouped summary |
| Failure semantics | Hybrid: baidu/local baseline and remote all-target failure are FAIL; hf/github direct failures can WARN until proxy also fails |
| Measurement command | Unified `curl --max-time 10 -L -o /dev/null -s -w ...` |
| Proxy trigger | Remote direct failure automatically opens `ssh -R` and retries via `ALL_PROXY` |

**User's choice:** `1b, 2c, 3c, 4a, 5a`
**Notes:** The user selected full-matrix defaults over a local-only default.

---

## Batch 2 — Remote Proxy Port, Tunnel Reuse, Heartbeat, Retry, Logs

| Question | Selected |
|----------|----------|
| Remote proxy port | Default `17890`, overridable |
| Tunnel lifecycle | Add reusable `net tunnel ensure --server X` for Phase 6 dependency |
| Heartbeat | Check both local ssh process and remote proxy curl |
| Retry | 3 retries with 1s/2s/4s backoff |
| Tunnel logs | JSON includes log path and redacted last 500 chars only |

**User's choice:** `6b, 7b, 8c, 9a, 10a`
**Notes:** This locks Phase 5 as the owner of reusable tunnel mechanics, not just one-shot probe fallback.

---

## Batch 3 — Local Proxy, Attempts, UAT Gate, Targets, Stdout

| Question | Selected |
|----------|----------|
| Local proxy fallback | Local direct-first; hf/github retry through `127.0.0.1:7890` if available |
| Direct/proxy attempts | One row per target with nested `attempts` |
| Completion gate | All configured servers must pass real UAT before Phase 5 completion |
| Target source | Read `config.network.targets` |
| Stdout format | Unique JSON only |

**User's choice:** `11b, 12b, 13a, 14a, 15a`
**Notes:** The completion gate is intentionally strict and may remain blocked while real SSH access is unavailable.

---

## Batch 4 — Agent-Recommended Defaults

| Question | Selected |
|----------|----------|
| Tunnel state | `~/.autoresearch/tunnels/<server>.json` |
| Existing tunnel | Reuse if heartbeat passes; rebuild if not |
| Local proxy URL | Default `http://127.0.0.1:7890`, overridable and redacted |
| Target curl retry | One direct attempt, one proxy attempt, no extra per-target retries |
| Target URL safety | Allow only http/https URLs with safe quoting |

**User's choice:** `推荐即可`
**Notes:** The user approved recommended defaults for the remaining low-risk implementation decisions.

---

## the agent's Discretion

- Exact module names, model names, progress stage names, grouped summary fields, and `curl -w` format.
- Whether to add `net tunnel status/stop` alongside `ensure` if the implementation uses a background supervisor.
- Which configured target to use for heartbeat when baidu is not present.

## Deferred Ideas

- Service reachability to local wandb/Prometheus is Phase 6.
- Training stack network dependence and dry runs are Phase 7.
- HTML/report visualization of network history belongs to later datalake/report phases.
